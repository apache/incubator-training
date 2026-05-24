# Apache Project Training Module Template

This is the template for creating training modules for Apache projects.
Copy this entire directory to create a new module.

## Quick Start

```bash
# 1. Copy the template
cp -r Template/ YourProject/

# 2. Update pom.xml (artifactId and name)
# 3. Replace project-logo.svg with your project's logo
# 4. Edit index.adoc — fill in all TODO sections
# 5. Build
cd YourProject
../../../mvnw process-resources -Drat.skip=true
open target/generated-slides/index.html
```

## Directory Structure

```
Template/
├── pom.xml                              # Maven build descriptor
├── metadata.yaml                        # Tags for catalog filtering
├── README.md                            # This file
└── src/
    └── main/
        ├── asciidoc/
        │   ├── _settings.adoc           # Reveal.js presentation settings
        │   ├── images/
        │   │   └── project-logo.svg     # YOUR PROJECT LOGO (required)
        │   └── index.adoc              # Main presentation content
        └── theme/
            └── apache.css              # Dark theme CSS (do not modify)
```

## Build Instructions

### Prerequisites

- Java 11+
- Maven (or use the included `mvnw` wrapper)

### First-Time Setup

Before building any module for the first time, install the shared tools:

```bash
cd /path/to/training/tools
../mvnw install
```

This installs the parent POM, shared resources (including the ASF oak leaf
logo), and the HTML template into your local Maven repository.

### Building a Module

```bash
cd content/Apache/YourProject
../../../mvnw process-resources -Drat.skip=true
```

The rendered HTML presentation will be at:
```
target/generated-slides/index.html
```

Open it directly in a browser — it's a self-contained reveal.js presentation.

**Important phases:**
- `generate-resources` — downloads reveal.js, copies theme/images (no slides yet)
- `process-resources` — converts AsciiDoc to HTML slides ← **use this one**
- `package` — full build including license checks (WAR output)

### Troubleshooting

| Problem | Fix |
|---------|-----|
| `Could not find artifact org.apache.training:training-tools:pom` | Run `mvnw install` from the `tools/` directory |
| RAT license check fails on `metadata.yaml` | Ensure the file has the ASF license header (see existing files) |
| Stale output after editing | Delete `target/` AND `.asciidoctor/` then rebuild |
| White background instead of dark | Ensure `src/main/theme/apache.css` is present (not modified) |

## Creating a New Module

### Step 1: Copy and Rename

```bash
cp -r content/Apache/Template/ content/Apache/YourProject/
```

### Step 2: Update `pom.xml`

Change these two lines:
```xml
<artifactId>training-content-apache-yourproject</artifactId>
<name>Training: Content: Apache: YourProject</name>
```

Keep the parent POM reference as-is (`1.5.0-SNAPSHOT`).

### Step 3: Add Your Project Logo

Replace `src/main/asciidoc/images/project-logo.svg` with your project's
actual logo. This appears in the **top-left corner** of every slide.

Get official logos from: https://apache.org/logos

Requirements:
- SVG format preferred (renders crisp at any size)
- Horizontal/landscape orientation works best (displayed at 120×36px)
- Filename must be exactly `project-logo.svg`

### Step 4: Update `metadata.yaml`

Fill in the project details and tags for the catalog:

```yaml
title: "Apache YourProject"
project_id: yourproject
description: "One-line description"
tags:
  - relevant-domain-tag
  - intro
  - developer
duration: "45-60 min"
level: beginner
language: java  # or python, scala, etc.
slides: 25
updated: "2026-01-01"
```

Standard tags:
- **Domain:** big-data, streaming, messaging, database, web, ml-ai, iot,
  build-tools, libraries, security, search, cloud, governance
- **Type:** intro, deep-dive, hands-on, overview
- **Ecosystem:** hadoop-ecosystem, jvm, python-ecosystem
- **Audience:** developer, operator, data-engineer, contributor

### Step 5: Write the Presentation Content

Edit `src/main/asciidoc/index.adoc`. The template has three parts:

1. **What is it?** (~8 slides) — problem it solves, features, architecture, use cases
2. **Installation & Getting Started** (~8 slides) — prerequisites, install, hello world
3. **Community Participation** (~8 slides) — channels, contributing, governance

## Slide Design Rules

### Content Limits Per Slide

These are hard rules — violating them causes text to overflow off-screen:

| Element | Maximum |
|---------|---------|
| Bullet points | 4–5 |
| Table rows | 4–5 |
| Code block lines | 8–10 |
| Lines of text total | 6–7 |

**If a slide has BOTH bullets AND an image, split into two slides.**

### When to Split

Split a slide when:
- Content would scroll below the visible area
- You have more than 5 bullet points
- **Never name the project chair** — it changes frequently and Apache is about community, not individuals. The governance slide can explain the PMC Chair *role* generically.
- A code example exceeds 10 lines
- A table has more than 5 rows
- You have an image plus more than 2 bullet points

### AsciiDoc Slide Syntax

```asciidoc
== Slide Title            ← creates a new slide (h2)

Bullet points:
* Point one
* Point two
* Point three

Code:
[source,bash]
----
echo "hello world"
----

Speaker notes (not shown on screen):
[.notes]
--
These notes are for the instructor only.
--
```

### Critical: No Preamble Content

**NEVER** put content before the first `==` section. In reveal.js, preamble
content becomes a persistent title that overlays every subsequent slide.

✅ Correct:
```asciidoc
include::_settings.adoc[]
:author: Your Name

== Apache YourProject        ← first slide

image::project-logo.svg[width=300]

Your tagline here
```

❌ Wrong (creates persistent overlay):
```asciidoc
include::_settings.adoc[]

[.text-center]
====
image::logo.svg[width=300]
Title text
====

== First Real Slide          ← too late, overlay already set
```

## Visual Theme

The presentation uses a dark theme optimized for conference rooms:

- **Background:** Dark (#1a1a1a)
- **Text:** White/light (#f0f0f0)
- **Font:** 32px base, Segoe UI / Helvetica / Arial
- **Headers:** Compact (h2 at 1.0em — same visual weight as body, just bold)
- **Code blocks:** Dark grey background with light text
- **Links:** Blue (#42affa)

### Logo Placement

| Logo | Position | Source |
|------|----------|--------|
| Project logo | Top-left (fixed) | `src/main/asciidoc/images/project-logo.svg` |
| ASF oak leaf | Bottom-left (fixed) | Shared resources (`logo-apache.png`) |

Both logos are fixed to the viewport — they don't scroll with content.

### Theme CSS

The file `src/main/theme/apache.css` provides the dark theme. **Do not modify
it** unless you want to diverge from the standard look. It overrides the
default white reveal.js theme and adds:

- Dark background on `.reveal-viewport`
- White text everywhere
- Compact headers
- Fixed-position logos
- Scroll overflow safety for long slides

## Catalog & Navigation

The site uses tag-based filtering instead of a giant nav menu:

1. Each module has a `metadata.yaml` with tags
2. Run `python3 tools/generate-catalog.py` to regenerate `catalog.json`
3. The catalog page (`site/src/site/asciidoc/catalog.adoc`) renders a
   filterable card grid

After adding a new module, always regenerate the catalog.

## License Headers

All source files need an Apache License 2.0 header:

- `.adoc` files: Use `////` comment blocks
- `.yaml` files: Use `#` comment lines
- `.css` files: Use `/* */` comment blocks
- `.xml` files: Use `<!-- -->` comment blocks

The RAT plugin checks this during `mvnw package`. Use `-Drat.skip=true`
during development to skip the check.
