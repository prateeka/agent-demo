# agent-demo

Destination launch agents — **files mode** (`launches/`) for hackathon; **Jira** is the target record layer.

See [README.md](README.md) and [platform/docs/FILES-MODEL.md](platform/docs/FILES-MODEL.md).

## For agents

- **Skills (committed, shared):** `platform/skills/destination-launch/`
- **IDE symlinks (committed):** only orchestrator in `.cursor/skills/` and `.claude/skills/` — run `./scripts/link-skills.sh` (verify with `ls -la .cursor/skills/`; do not execute the symlink path in a shell)
- **Step skills:** `platform/skills/destination-launch/steps/` — child agents only, not in skill picker
- **Entry point:** orchestrator — `platform/skills/destination-launch/orchestrator/SKILL.md`
- **Create/update** `launches/{slug}/` — `epic.md`, `tasks/{step_id}.md` (not Jira for now)
- **Workflow:** `platform/workflow.yaml`
- **Global context:** children return `global_keys` YAML; orchestrator merges into `epic.md` (no key registry file yet)
- **Spawn child agents** for step work; never execute steps inline in orchestrator chat
- **Code repos:** set `LAUNCHPAD_DIST` / `LAUNCHPAD_DIST_TYPES` before implementation steps — see `platform/config/repos.yaml`

## Sibling repos

Override with env vars or edit `repos.yaml`:

```bash
export LAUNCHPAD_DIST=/path/to/dist
export LAUNCHPAD_DIST_TYPES=/path/to/dist_types
```
