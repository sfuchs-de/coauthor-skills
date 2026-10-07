#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const ORDERING_TYPES = new Set(["defines", "requires", "feeds"]);
const EDGE_TYPES = new Set([
  ...ORDERING_TYPES,
  "joint",
  "specializes",
  "extends",
  "verifies",
  "conflicts-with",
  "supersedes",
]);
const STATUS_TYPES = new Set(["final", "review", "draft", "unknown"]);
const OWNED_KINDS = new Set([
  "lemma",
  "identity",
  "result",
  "equilibrium",
  "computation",
  "estimation",
  "benchmark",
  "extension",
  "frontier",
]);

function usage(exitCode = 0) {
  console.log(`Usage:
  validate_dependency_graph.mjs --graph FILE [options]

Required:
  --graph FILE          Dependency graph JSON

Options:
  --require-owners      Require owners for formal result-like nodes
  --require-sources     Require source_anchors for every node
  --require-reasons     Require a nonempty reason on every edge and joint block
  --print-order         Print topological levels after validation
  --mermaid             Print a Mermaid view after validation
  --help                Show this help
`.trimEnd());
  process.exit(exitCode);
}

function parseArgs(argv) {
  const values = new Map();
  const flags = new Set();
  const boolean = new Set([
    "help",
    "require-owners",
    "require-sources",
    "require-reasons",
    "print-order",
    "mermaid",
  ]);
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) throw new Error(`Unexpected argument: ${token}`);
    const key = token.slice(2);
    if (boolean.has(key)) {
      flags.add(key);
      continue;
    }
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for --${key}`);
    values.set(key, value);
    i += 1;
  }
  return { values, flags };
}

function nonemptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isStringArray(value) {
  return Array.isArray(value) && value.every(nonemptyString);
}

function stronglyConnectedComponents(vertices, adjacency) {
  let index = 0;
  const stack = [];
  const onStack = new Set();
  const indices = new Map();
  const lowLink = new Map();
  const components = [];

  function visit(vertex) {
    indices.set(vertex, index);
    lowLink.set(vertex, index);
    index += 1;
    stack.push(vertex);
    onStack.add(vertex);

    for (const next of adjacency.get(vertex) ?? []) {
      if (!indices.has(next)) {
        visit(next);
        lowLink.set(vertex, Math.min(lowLink.get(vertex), lowLink.get(next)));
      } else if (onStack.has(next)) {
        lowLink.set(vertex, Math.min(lowLink.get(vertex), indices.get(next)));
      }
    }

    if (lowLink.get(vertex) === indices.get(vertex)) {
      const component = [];
      while (stack.length > 0) {
        const member = stack.pop();
        onStack.delete(member);
        component.push(member);
        if (member === vertex) break;
      }
      components.push(component);
    }
  }

  for (const vertex of vertices) {
    if (!indices.has(vertex)) visit(vertex);
  }
  return components;
}

function topologicalLevels(vertices, adjacency) {
  const indegree = new Map([...vertices].map((vertex) => [vertex, 0]));
  for (const from of vertices) {
    for (const to of adjacency.get(from) ?? []) {
      indegree.set(to, indegree.get(to) + 1);
    }
  }

  let frontier = [...vertices].filter((vertex) => indegree.get(vertex) === 0).sort();
  const levels = [];
  let visited = 0;
  while (frontier.length > 0) {
    levels.push(frontier);
    visited += frontier.length;
    const nextFrontier = [];
    for (const from of frontier) {
      for (const to of adjacency.get(from) ?? []) {
        indegree.set(to, indegree.get(to) - 1);
        if (indegree.get(to) === 0) nextFrontier.push(to);
      }
    }
    frontier = [...new Set(nextFrontier)].sort();
  }
  return { levels, visited };
}

function mermaid(graph, nodeMap) {
  const ids = new Map(graph.nodes.map((node, index) => [node.id, `N${index}`]));
  const escape = (value) => String(value).replaceAll("\\", "\\\\").replaceAll('"', "'");
  const lines = ["flowchart TD"];
  for (const node of graph.nodes) {
    lines.push(`  ${ids.get(node.id)}["${escape(node.title)}"]`);
  }
  for (const edge of graph.edges) {
    const from = ids.get(edge.from);
    const to = ids.get(edge.to);
    if (!from || !to) continue;
    const label = escape(edge.type);
    const arrow = ORDERING_TYPES.has(edge.type) ? `-->|${label}|` : `-.->|${label}|`;
    lines.push(`  ${from} ${arrow} ${to}`);
  }
  for (const block of graph.joint_blocks ?? []) {
    lines.push(`  %% joint block ${escape(block.id)}: ${block.members.map((id) => escape(nodeMap.get(id)?.title ?? id)).join(", ")}`);
  }
  return lines.join("\n");
}

function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    usage(2);
  }
  if (args.flags.has("help")) usage(0);
  const graphArg = args.values.get("graph");
  if (!graphArg) usage(2);
  const graphFile = path.resolve(graphArg);
  if (!fs.existsSync(graphFile)) throw new Error(`Graph file not found: ${graphFile}`);

  let graph;
  try {
    graph = JSON.parse(fs.readFileSync(graphFile, "utf8"));
  } catch (error) {
    throw new Error(`Invalid graph JSON: ${error.message}`);
  }

  const errors = [];
  const warnings = [];
  if (!Array.isArray(graph.nodes)) errors.push("nodes must be an array");
  if (!Array.isArray(graph.edges)) errors.push("edges must be an array");
  if (errors.length > 0) {
    for (const error of errors) console.error(`ERROR ${error}`);
    process.exit(1);
  }

  const nodeMap = new Map();
  for (const [index, node] of graph.nodes.entries()) {
    const where = `nodes[${index}]`;
    if (!nonemptyString(node.id)) {
      errors.push(`${where}: id is required`);
      continue;
    }
    if (/\s/.test(node.id)) errors.push(`${where}: id must not contain whitespace: ${node.id}`);
    if (nodeMap.has(node.id)) errors.push(`${where}: duplicate node id ${node.id}`);
    nodeMap.set(node.id, node);
    if (!nonemptyString(node.title)) errors.push(`${where}: title is required`);
    if (!nonemptyString(node.kind)) errors.push(`${where}: kind is required`);
    if (node.status && !STATUS_TYPES.has(String(node.status).toLowerCase())) {
      errors.push(`${where}: unsupported status ${node.status}`);
    }
    for (const field of ["inputs", "outputs", "assumptions", "source_anchors", "verification", "open_issues"]) {
      if (node[field] !== undefined && !isStringArray(node[field])) {
        errors.push(`${where}: ${field} must be an array of nonempty strings`);
      }
    }
    if (
      args.flags.has("require-owners")
      && OWNED_KINDS.has(String(node.kind).toLowerCase())
      && !nonemptyString(node.owner)
    ) {
      errors.push(`${where}: formal node ${node.id} requires an owner`);
    }
    if (
      args.flags.has("require-sources")
      && (!isStringArray(node.source_anchors) || node.source_anchors.length === 0)
    ) {
      errors.push(`${where}: node ${node.id} requires source_anchors`);
    }
  }

  const edgeKeys = new Set();
  const incident = new Map([...nodeMap.keys()].map((id) => [id, 0]));
  for (const [index, edge] of graph.edges.entries()) {
    const where = `edges[${index}]`;
    if (!nodeMap.has(edge.from)) errors.push(`${where}: unresolved from node ${edge.from}`);
    if (!nodeMap.has(edge.to)) errors.push(`${where}: unresolved to node ${edge.to}`);
    if (!EDGE_TYPES.has(edge.type)) errors.push(`${where}: unsupported edge type ${edge.type}`);
    if (edge.from === edge.to) errors.push(`${where}: self edge on ${edge.from}`);
    if (args.flags.has("require-reasons") && !nonemptyString(edge.reason)) {
      errors.push(`${where}: edge requires a reason`);
    }
    const key = `${edge.from}\u0000${edge.to}\u0000${edge.type}`;
    if (edgeKeys.has(key)) errors.push(`${where}: duplicate edge ${edge.from} -> ${edge.to} (${edge.type})`);
    edgeKeys.add(key);
    if (incident.has(edge.from)) incident.set(edge.from, incident.get(edge.from) + 1);
    if (incident.has(edge.to)) incident.set(edge.to, incident.get(edge.to) + 1);
  }

  const blocks = Array.isArray(graph.joint_blocks) ? graph.joint_blocks : [];
  if (graph.joint_blocks !== undefined && !Array.isArray(graph.joint_blocks)) {
    errors.push("joint_blocks must be an array");
  }
  const blockMap = new Map();
  const memberBlock = new Map();
  for (const [index, block] of blocks.entries()) {
    const where = `joint_blocks[${index}]`;
    if (!nonemptyString(block.id)) {
      errors.push(`${where}: id is required`);
      continue;
    }
    if (blockMap.has(block.id)) errors.push(`${where}: duplicate joint block ${block.id}`);
    blockMap.set(block.id, block);
    if (!Array.isArray(block.members) || block.members.length < 2) {
      errors.push(`${where}: joint block needs at least two members`);
      continue;
    }
    if (new Set(block.members).size !== block.members.length) {
      errors.push(`${where}: duplicate member in joint block ${block.id}`);
    }
    if (args.flags.has("require-reasons") && !nonemptyString(block.reason)) {
      errors.push(`${where}: joint block requires a reason`);
    }
    for (const member of block.members) {
      if (!nodeMap.has(member)) errors.push(`${where}: unresolved member ${member}`);
      if (memberBlock.has(member)) {
        errors.push(`${where}: node ${member} belongs to multiple joint blocks`);
      }
      memberBlock.set(member, block.id);
    }
  }

  for (const [index, edge] of graph.edges.entries()) {
    if (edge.type === "joint") {
      const fromBlock = memberBlock.get(edge.from);
      const toBlock = memberBlock.get(edge.to);
      if (!fromBlock || fromBlock !== toBlock) {
        errors.push(`edges[${index}]: joint edge endpoints must share one declared joint block`);
      }
    }
    if (ORDERING_TYPES.has(edge.type)) {
      const fromBlock = memberBlock.get(edge.from);
      const toBlock = memberBlock.get(edge.to);
      if (fromBlock && fromBlock === toBlock) {
        errors.push(`edges[${index}]: ordering edge inside joint block ${fromBlock}; use joint`);
      }
    }
  }

  const modules = Array.isArray(graph.modules) ? graph.modules : [];
  if (graph.modules !== undefined && !Array.isArray(graph.modules)) {
    errors.push("modules must be an array");
  }
  const moduleMap = new Map();
  const nodeModules = new Map();
  const claimedByModule = new Map();
  for (const [index, module] of modules.entries()) {
    const where = `modules[${index}]`;
    if (!nonemptyString(module.id)) {
      errors.push(`${where}: id is required`);
      continue;
    }
    if (moduleMap.has(module.id)) errors.push(`${where}: duplicate module ${module.id}`);
    moduleMap.set(module.id, module);
    if (!Array.isArray(module.nodes) || module.nodes.length === 0) {
      errors.push(`${where}: nodes must be a nonempty array`);
    } else {
      for (const nodeId of module.nodes) {
        if (!nodeMap.has(nodeId)) errors.push(`${where}: unresolved node ${nodeId}`);
        if (!nodeModules.has(nodeId)) nodeModules.set(nodeId, []);
        nodeModules.get(nodeId).push(module.id);
      }
    }
    for (const claimId of module.owned_claims ?? []) {
      if (!nodeMap.has(claimId)) errors.push(`${where}: unresolved owned claim ${claimId}`);
      if (claimedByModule.has(claimId)) {
        errors.push(`${where}: claim ${claimId} owned by multiple modules`);
      }
      claimedByModule.set(claimId, module.id);
      const nodeOwner = nodeMap.get(claimId)?.owner;
      if (nodeOwner && nodeOwner !== module.id) {
        errors.push(`${where}: claim ${claimId} owner ${nodeOwner} disagrees with module ${module.id}`);
      }
    }
  }

  if (modules.length > 0) {
    for (const node of graph.nodes) {
      if (OWNED_KINDS.has(String(node.kind).toLowerCase()) && !nodeModules.has(node.id)) {
        warnings.push(`formal node ${node.id} is not assigned to a module`);
      }
      if (node.owner && !moduleMap.has(node.owner)) {
        warnings.push(`node ${node.id} owner ${node.owner} is not declared in modules[]`);
      }
    }
  }

  for (const [nodeId, count] of incident) {
    if (graph.nodes.length > 1 && count === 0) warnings.push(`orphan node ${nodeId}`);
  }

  const entityFor = (nodeId) => memberBlock.has(nodeId) ? `@${memberBlock.get(nodeId)}` : nodeId;
  const entities = new Set([
    ...graph.nodes.filter((node) => !memberBlock.has(node.id)).map((node) => node.id),
    ...blocks.map((block) => `@${block.id}`),
  ]);
  const adjacency = new Map([...entities].map((entity) => [entity, new Set()]));
  for (const edge of graph.edges) {
    if (!ORDERING_TYPES.has(edge.type)) continue;
    if (!nodeMap.has(edge.from) || !nodeMap.has(edge.to)) continue;
    const from = entityFor(edge.from);
    const to = entityFor(edge.to);
    if (from !== to) adjacency.get(from)?.add(to);
  }

  const components = stronglyConnectedComponents(entities, adjacency);
  for (const component of components) {
    if (component.length > 1) {
      errors.push(`ordering cycle: ${component.sort().join(" -> ")}`);
    }
  }
  const topo = topologicalLevels(entities, adjacency);
  if (topo.visited !== entities.size) errors.push("ordering graph is not acyclic");

  const describeEntity = (entity) => {
    if (entity.startsWith("@")) {
      const block = blockMap.get(entity.slice(1));
      return `${block?.id ?? entity} [joint: ${(block?.members ?? []).join(", ")}]`;
    }
    return `${entity} [${nodeMap.get(entity)?.kind ?? "unknown"}]`;
  };

  console.log(
    `nodes=${graph.nodes.length} edges=${graph.edges.length} joint_blocks=${blocks.length} modules=${modules.length} levels=${topo.levels.length}`,
  );
  for (const warning of warnings) console.warn(`WARN ${warning}`);
  if (errors.length > 0) {
    for (const error of errors) console.error(`ERROR ${error}`);
    process.exit(1);
  }

  console.log("Theory dependency graph validation: PASS");
  if (args.flags.has("print-order")) {
    topo.levels.forEach((level, index) => {
      console.log(`Level ${index + 1}: ${level.map(describeEntity).join("; ")}`);
    });
  }
  if (args.flags.has("mermaid")) {
    console.log("\n```mermaid");
    console.log(mermaid(graph, nodeMap));
    console.log("```");
  }
}

try {
  main();
} catch (error) {
  console.error(`ERROR ${error.message}`);
  process.exit(1);
}
