/**
 * Container-side runtime registry.
 *
 * Each SDK runtime (Claude, Codex) self-registers its query handler.
 * The main loop dispatches to the registered handler based on ContainerInput.runtime.
 */
import type { ContainerInput } from './shared.js';

export interface QueryResult {
  newSessionId?: string;
  lastAssistantUuid?: string;
  closedDuringQuery: boolean;
}

export type RuntimeHandler = (
  prompt: string,
  sessionId: string | undefined,
  mcpServerPath: string,
  containerInput: ContainerInput,
  sdkEnv: Record<string, string | undefined>,
  resumeAt?: string,
) => Promise<QueryResult>;

const registry = new Map<string, RuntimeHandler>();

export function registerContainerRuntime(
  name: string,
  handler: RuntimeHandler,
): void {
  registry.set(name, handler);
}

export function getContainerRuntime(
  name: string,
): RuntimeHandler | undefined {
  return registry.get(name);
}

export function getRegisteredContainerRuntimeNames(): string[] {
  return [...registry.keys()];
}
