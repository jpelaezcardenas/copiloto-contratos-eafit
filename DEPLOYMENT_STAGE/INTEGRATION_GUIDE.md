# INTEGRATION GUIDE — Cómo Integrar OpenSpec + Deployment a Todos Tus Proyectos

**Objetivo:** Llevar el estándar de deployment a los 8 proyectos en `C:\Users\contexia\Projects\` y a todas las plataformas (Claude Code, Antigravity IDE, Antigravity 2.0, Codex).

---

## Fase 1: Setup Global (30 min)

### 1.1 Crear Symlink Global en `.antigravity/`

```bash
cd C:\Users\contexia
mkdir -p .antigravity
ln -s Projects/ai-specs/openspec-deployment-standard .antigravity/deployment-standard
# Verifica
ls -la .antigravity/deployment-standard/
```

**Resultado:** `.antigravity/deployment-standard/` apunta a la fuente única de verdad.

---

### 1.2 Actualizar Global CLAUDE.md

Abre `C:\Users\contexia\.claude\CLAUDE.md` y añade esta sección:

```markdown
## OpenSpec Deployment Gate (ALL PROJECTS & PLATFORMS)

**Standard location:** `ai-specs/openspec-deployment-standard/`

Every OpenSpec change must include Stage 11: Deploy to Production.

Before archiving ANY change:
1. Execute Stage 11 (see DEPLOYMENT_STAGE.md)
2. Verify changes are LIVE at production URL
3. Create deployment report in openspec/changes/[CHANGE-ID]/reports/
4. Only then `/opsx:archive`

Platforms covered:
- Claude Code (.claude/)
- Antigravity IDE (.antigravity/)
- Antigravity 2.0 (.antigravity2/)
- Codex (via shared CLAUDE.md)
- Contexia Global (C:\Users\contexia\Projects)

Self-improving loop: Every time deployment fails, reviewer updates CHECKPOINTS.md.
```

---

## Fase 2: Por Proyecto (5 min por proyecto × 8 = 40 min)

Para **cada proyecto** en `C:\Users\contexia\Projects\`:

### 2.1 Crear Symlink Proyecto → Global

```bash
cd antigravity-app
ln -s ../ai-specs/openspec-deployment-standard DEPLOYMENT_STAGE
# Verifica
ls -la DEPLOYMENT_STAGE/
```

Repite para:
- contexia-landing-deploy
- contexia-ops-template
- copiloto-contratos-eafit

**Proyectos removidos 2026-05-30:**
- ~~antigravity-app-taty-fiscal-telegram-rag~~ (was redundant worktree)
- ~~contexia-app-stitch~~ (no longer in use)
- ~~contexia-social-ops~~ (was redundant worktree)
- ~~temp_pwa~~ (unused PWA without code)

### 2.2 Actualizar CLAUDE.md del Proyecto

Abre `[proyecto]/CLAUDE.md` y **reemplaza o añade:**

```markdown
## 7. OpenSpec Deployment Stage

All OpenSpec changes require Stage 11: Deploy to Production.

Reference: `DEPLOYMENT_STAGE/` (symlink to ai-specs/openspec-deployment-standard/)

### Project-Specific Details

**Repository:** [repo-url]
**Deploy branch:** main
**Frontend deploy:** Vercel (if applicable)
  - URL: https://contexia.online/app/[section]
  - Checklist: DEPLOYMENT_STAGE/checklist-vercel.md

**Backend deploy:** Railway (if applicable)
  - URL: https://[project]-production-[id].up.railway.app
  - Checklist: DEPLOYMENT_STAGE/checklist-railway.md

**Database:** Supabase (if applicable)
  - Migrations folder: apps/backend/migrations/
  - Validation: `npm run migrate:test`

### Stage 11 Template for tasks.md

Add this to every new OpenSpec change's tasks.md:

## Stage 11. Deploy to Production (MANDATORY - CLOSES THE LOOP)

See: `DEPLOYMENT_STAGE/DEPLOYMENT_STAGE.md`

- [ ] 11.1 git commit + push to `[deploy-branch]`
- [ ] 11.2 Vercel build complete (if frontend change)
- [ ] 11.3 Railway deploy active (if backend change)
- [ ] 11.4 Production URL: changes visible and verified
- [ ] 11.5 Deployment report: openspec/changes/[CHANGE-ID]/reports/YYYY-MM-DD-deployment.md
```

---

## Fase 3: Plataformas de Desarrollo (30 min)

### 3.1 Claude Code

Archivo: `.claude/CLAUDE.md` (en la raíz del repo)

**Ya cubierto en Fase 2.2** — simplemente sigue el template.

**Validación:**
```bash
cat antigravity-app/.claude/CLAUDE.md | grep -A 5 "Deploy"
# Debería mostrar la sección de deployment
```

---

### 3.2 Antigravity IDE

Archivo: `.antigravity/CLAUDE.md` (si existe, sino créalo)

```bash
cd antigravity-app
cat > .antigravity/CLAUDE.md << 'EOF'
# Antigravity IDE — OpenSpec + Deployment

This IDE is for antigravity-app development.

## Standard Workflow

1. Open OpenSpec change: openspec/changes/[CHANGE-ID]/
2. Follow tasks.md (including Stage 11: Deploy)
3. Reference: DEPLOYMENT_STAGE/ for deployment checklists
4. After deployment, create report in reports/ folder
5. Then archive the change

## Key Files

- DEPLOYMENT_STAGE/ → symlink to deployment standard
- .antigravity/CLAUDE.md → this file
- See .claude/CLAUDE.md for full details

## Tools

- Vercel dashboard: https://vercel.com/contexia/antigravity-app/deployments
- Railway dashboard: https://railway.app/[project]/deployments
- GitHub: https://github.com/jpelaezcardenas/antigravity-app
EOF
```

---

### 3.3 Antigravity 2.0

Archivo: `.antigravity2/CLAUDE.md` (o equivalente)

```bash
# Asume que Antigravity 2.0 está en el mismo directorio
# o en C:\Users\contexia\antigravity-2.0
mkdir -p .antigravity2
cat > .antigravity2/CLAUDE.md << 'EOF'
# Antigravity 2.0 IDE — OpenSpec + Deployment

This is the enhanced version of Antigravity IDE.

All workflows follow: C:\Users\contexia\.antigravity/deployment-standard/

See .claude/CLAUDE.md in your project root for full setup.
EOF
```

---

### 3.4 Codex (ChatGPT)

Archivo: `ai-specs/codex-context.md` (nueva)

```bash
cat > C:\Users\contexia\Projects\ai-specs\codex-context.md << 'EOF'
# Codex (ChatGPT) Context — OpenSpec + Deployment

**When using Codex for antigravity-app development:**

Paste this at the start of your Codex chat:

---

I'm developing antigravity-app using OpenSpec framework.

### Key Standard
All OpenSpec changes must include Stage 11: Deploy to Production.

Reference files (in the repo):
- DEPLOYMENT_STAGE/DEPLOYMENT_STAGE.md — full deployment workflow
- DEPLOYMENT_STAGE/checklist-vercel.md — if frontend change
- DEPLOYMENT_STAGE/checklist-railway.md — if backend change
- CHECKPOINTS.md — objective criteria for "done"

### Before Archiving
1. Execute all tasks including Stage 11
2. Verify changes LIVE at https://contexia.online/app/bunker
3. Create report in openspec/changes/[CHANGE-ID]/reports/YYYY-MM-DD-deployment.md
4. Then /opsx:archive

### Key URLs
- Vercel: https://vercel.com/contexia/antigravity-app/deployments
- Railway: https://railway.app/[project]/deployments
- Production: https://contexia.online/app/bunker

---

Always reference the deployment checklists before declaring Stage 11 done.
EOF
```

---

## Fase 4: Validación (20 min)

### 4.1 Verifica Symlinks

```bash
cd C:\Users\contexia\Projects

# Antigravity-app
ls -la antigravity-app/DEPLOYMENT_STAGE/DEPLOYMENT_STAGE.md
# Debería mostrar: → ../ai-specs/openspec-deployment-standard/DEPLOYMENT_STAGE.md

# Otros proyectos
for dir in antigravity-app-taty-fiscal-telegram-rag contexia-app-stitch contexia-landing-deploy contexia-ops-template contexia-social-ops copiloto-contratos-eafit temp_pwa; do
  if [ -L "$dir/DEPLOYMENT_STAGE" ]; then
    echo "✅ $dir: symlink OK"
  else
    echo "❌ $dir: symlink missing or broken"
  fi
done
```

### 4.2 Verifica CLAUDE.md

```bash
# Verifica que cada proyecto tiene deployment section
for dir in antigravity-app contexia-app-stitch; do
  echo "=== $dir ==="
  grep -A 3 "Deploy" "$dir/CLAUDE.md" | head -5
done
```

### 4.3 Prueba Walkthrough en Un Proyecto

**Proyecto piloto:** antigravity-app

1. Abre Claude Code en antigravity-app
2. Lee DEPLOYMENT_STAGE/DEPLOYMENT_STAGE.md
3. Verifica que entiendes Stage 11
4. Responde: "¿Qué es Stage 11 en OpenSpec?"
5. Si Claude responde correctamente, estás listo

---

## Fase 5: Documentación (15 min)

### 5.1 Crear GLOBAL_DEPLOYMENT_STANDARD.md

```bash
cat > C:\Users\contexia\.antigravity\GLOBAL_DEPLOYMENT_STANDARD.md << 'EOF'
# Contexia Global — OpenSpec + Deployment Standard

**Location:** C:\Users\contexia\Projects\ai-specs\openspec-deployment-standard\

**Applies to:** All 8 projects in Contexia workspace

## Quick Reference

| Step | File | Applies to |
|------|------|-----------|
| Stage 11: Deploy | DEPLOYMENT_STAGE.md | ALL |
| Vercel checklist | checklist-vercel.md | Frontend projects |
| Railway checklist | checklist-railway.md | Backend projects |
| Criteria | CHECKPOINTS.md | ALL |

## Projects Covered

1. antigravity-app (frontend + backend)
2. antigravity-app-taty-fiscal-telegram-rag
3. contexia-app-stitch
4. contexia-landing-deploy
5. contexia-ops-template
6. contexia-social-ops
7. copiloto-contratos-eafit
8. temp_pwa

## Deployment URLs

- Vercel dashboard: https://vercel.com/contexia
- Railway dashboard: https://railway.app/[projects]
- Production frontend: https://contexia.online

## Self-Improving Loop

Every time a reviewer rejects deployment for a new reason:
1. Add rule to CHECKPOINTS.md
2. Next projects inherit that rule
3. Iterate

---

**Last updated:** [TODAY]
**Source of truth:** ai-specs/openspec-deployment-standard/
EOF
```

### 5.2 Actualizar MEMORY.md

Abre `C:\Users\contexia\.claude\MEMORY.md` y añade:

```markdown
## OpenSpec + Deployment Standard (2026-05-30)

Implementado standard global para **ALL 8 proyectos** y **plataformas** (Claude Code, Antigravity IDE, Antigravity 2.0, Codex).

- **Fuente única:** `ai-specs/openspec-deployment-standard/`
- **Stage 11:** Obligatorio en todos los OpenSpec changes
- **CHECKPOINTS.md:** Criterios objetivos de "done" + self-improving loop
- **Checklists:** Vercel + Railway específicos
- **Symlinks:** Cada proyecto apunta a global (ai-specs/)

Cierra el gap: OpenSpec archive ≠ producción. Ahora:
  proposal → design → spec → tasks → apply → [DEPLOY] → archive

**Validación:** antigravity-app primero, luego 7 proyectos más.
```

---

## Fase 6: Ejecución (Próxima Semana)

### 6.1 Primer Test: antigravity-app

```bash
cd antigravity-app

# 1. Lee la guía
cat DEPLOYMENT_STAGE/DEPLOYMENT_STAGE.md | head -50

# 2. Abre un OpenSpec change existente (o crea uno nuevo)
ls openspec/changes/

# 3. Añade Stage 11 a tasks.md (si no lo tiene)

# 4. Ejecuta stage 11 (git push, Vercel, etc.)

# 5. Crea reporte
mkdir -p openspec/changes/[CHANGE-ID]/reports
cat > openspec/changes/[CHANGE-ID]/reports/YYYY-MM-DD-deployment.md << 'EOF'
# Deployment Report — [CHANGE-ID]
...
EOF

# 6. Verifica
git status --short
```

### 6.2 Replicación a Otros 7 Proyectos

Una vez que antigravity-app funciona:
- Copia CLAUDE.md section (Stage 11) a otros 7
- Crea symlinks (ya hechos)
- Prueba con un pequeño cambio en 1-2 proyectos

---

## Checklist Final

- [ ] Global symlink en `.antigravity/deployment-standard/` ✅
- [ ] Global CLAUDE.md actualizado ✅
- [ ] 8 proyectos: symlink `DEPLOYMENT_STAGE/` ✅
- [ ] 8 proyectos: `CLAUDE.md` actualizado ✅
- [ ] `.antigravity/CLAUDE.md` creado ✅
- [ ] `.antigravity2/CLAUDE.md` creado ✅
- [ ] `ai-specs/codex-context.md` creado ✅
- [ ] `GLOBAL_DEPLOYMENT_STANDARD.md` en `.antigravity/` ✅
- [ ] `MEMORY.md` actualizado ✅
- [ ] Validación: symlinks y CLAUDE.md ✅
- [ ] Test: antigravity-app funciona ✅
- [ ] Git commit de toda la setup ✅

---

## Git Commit

```bash
cd C:\Users\contexia\Projects

git add ai-specs/openspec-deployment-standard/
git add -A  # .antigravity/*, **/CLAUDE.md updates, etc.
git commit -m "feat: openspec deployment standard for all projects

- Created ai-specs/openspec-deployment-standard/ with:
  - DEPLOYMENT_STAGE.md: full workflow
  - CHECKPOINTS.md: objective criteria + self-improving loop
  - checklist-vercel.md: frontend deployment
  - checklist-railway.md: backend deployment
  - INTEGRATION_GUIDE.md: how to apply globally

- Applied to all 8 projects:
  - antigravity-app
  - antigravity-app-taty-fiscal-telegram-rag
  - contexia-app-stitch
  - contexia-landing-deploy
  - contexia-ops-template
  - contexia-social-ops
  - copiloto-contratos-eafit
  - temp_pwa

- Covered all development platforms:
  - Claude Code (.claude/CLAUDE.md)
  - Antigravity IDE (.antigravity/CLAUDE.md)
  - Antigravity 2.0 (.antigravity2/CLAUDE.md)
  - Codex (ai-specs/codex-context.md)

Closes the gap: OpenSpec archive now includes mandatory Stage 11 (Deploy).
Self-improving loop: CHECKPOINTS.md evolves based on reviewer feedback."

git push
```

---

## ¿Qué sigue?

Una vez todo esté en lugar:

1. **Antigravity-app:** Próximo OpenSpec change incluye Stage 11 → deploy a producción
2. **Otros 7 proyectos:** El siguiente cambio en cada uno también incluye Stage 11
3. **Ciclo de mejora:** Cada rechazo de deploy → actualiza CHECKPOINTS.md

En 2-3 meses, CHECKPOINTS.md será un resumen brutal de todo lo que aprendiste sobre deployment.
