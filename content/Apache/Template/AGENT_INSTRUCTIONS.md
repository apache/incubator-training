# Agent Instructions: Generating a New Training Module

These instructions are for an AI agent tasked with generating a new Apache
project training presentation from the Template. Follow them exactly.

## Overview

You are generating a reveal.js AsciiDoc presentation for an Apache project.
The output must build cleanly with Maven and render as a dark-themed slide
deck viewable in a browser.

## CRITICAL: Research First, Write Second

**DO NOT rely on training data or general knowledge for ANY project-specific
facts.** Your training data is stale and often wrong. Projects rename things,
spin off sub-projects, change installation steps, and deprecate features
constantly. You MUST research every claim by fetching live documentation.

### Research Phase (MANDATORY — do this BEFORE writing any slides)

For each presentation, you must fetch and read the following pages:

1. **Project homepage** — `https://PROJECT_ID.apache.org`
   - What does the project call itself? (Don't assume — projects rename)
   - What is the current tagline/description in their own words?
   - What sub-projects or components exist? Are any now separate TLPs?

2. **Getting Started / Quick Start page** — find this from the homepage nav
   - What are the actual prerequisites?
   - What are the exact install commands?
   - What does the first-run experience look like?
   - What port does it run on? What's the default URL?

3. **Download page** — `https://PROJECT_ID.apache.org/download` or similar
   - What is the current version?
   - What package formats are available?
   - Is there a Docker image? What's its exact name?

4. **Community / Contributing page**
   - What are the actual mailing list addresses?
   - Where is the issue tracker? (Jira? GitHub Issues? Both?)
   - Where is the source code? (GitHub? GitBox? Multiple repos?)

5. **Apache committee data** — use the apache_projects tools to verify:
   - Is this project still an active TLP? (Check it hasn't retired to Attic)
   - How many PMC members / committers?
   - When was it established?
   - Are there related projects that have split off?

### Content Rules Based on Research

- Use the EXACT terminology the project uses on their website
- If the project calls something "XYZ" on their docs, use "XYZ" — not what
  you think it "used to be" or "should be" called
- If you cannot verify a fact from a live source, DO NOT include it
- When in doubt, leave a TODO comment for human review:
  `// TODO: Verify this against PROJECT_ID.apache.org — could not confirm`

### Human Review Required

Every generated presentation MUST be reviewed by a human familiar with the
project before it is published. The agent's job is to produce a well-structured
draft with researched content — but mistakes will happen, and only someone
who uses the project can catch subtle errors in terminology, architecture
descriptions, or getting-started flows.

Flag anything uncertain with a comment:
```asciidoc
// TODO: Human review — verify this is still the correct install process
```

## File Structure to Create

Copy the Template directory and produce these files:

```
content/Apache/<ProjectName>/
├── pom.xml
├── metadata.yaml
└── src/
    └── main/
        ├── asciidoc/
        │   ├── _settings.adoc       (copy from Template, do not modify)
        │   ├── images/
        │   │   └── project-logo.png  (download from https://apache.org/logos/res/<project_id>/default.png)
        │   └── index.adoc            (the presentation — YOU WRITE THIS)
        └── theme/
            └── apache.css            (copy from Template, do not modify)
```

## pom.xml

Use this exact structure (only change the artifactId and name):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>org.apache.training</groupId>
    <artifactId>content-parent-pom</artifactId>
    <version>1.5.0-SNAPSHOT</version>
    <relativePath>../../../tools/content-parent-pom/pom.xml</relativePath>
  </parent>

  <groupId>org.apache.training.content</groupId>
  <artifactId>training-content-apache-PROJECT_ID</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>war</packaging>

  <name>Training: Content: Apache: PROJECT_NAME</name>
  <description>Training module for Apache PROJECT_NAME</description>

</project>
```

## metadata.yaml

Must have the ASF license header. Example:

```yaml
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

title: "Apache PROJECT_NAME"
project_id: PROJECT_ID
description: "One-line description"
tags:
  - relevant-tag
  - intro
  - developer
duration: "45-60 min"
level: beginner
language: java
slides: 25
updated: "YYYY-MM-DD"
```

## index.adoc — THE PRESENTATION

This is where all the content goes. Follow these rules EXACTLY:

### Rule 1: ASF License Header

The file MUST start with:

```asciidoc
////

  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  ...full header...

////
```

### Rule 2: Settings Include

Immediately after the license header:

```asciidoc
include::_settings.adoc[]
:presenter_name: Your Name
:presenter_company: Your Company
:description: Introduction to Apache PROJECT_NAME
:keywords: Apache, PROJECT_NAME
:author: Your Name
:email: Your email
:position: Your role
```

DO NOT add `:revealjsdir:`, `:revealjs_slideNumber:`, or `:revealjs_theme:`
attributes. Maven handles all of these.

### Rule 3: NO PREAMBLE — Title Slide is the First == Section

**CRITICAL**: The FIRST content after the attributes MUST be a `==` section.
NEVER put content (images, text, blocks) before the first `==`.

Content before `==` becomes a PERSISTENT overlay on every slide. This is the
single most common mistake.

✅ CORRECT:
```asciidoc
== Apache PROJECT_NAME

image::project-logo.png[Apache PROJECT_NAME, 500]

*Your project tagline here*
```

❌ WRONG (creates persistent overlay on ALL slides):
```asciidoc
[.text-center]
====
image::logo.png[width=400]
Title
====

== First Slide
```

❌ ALSO WRONG (= creates document title/preamble):
```asciidoc
= Apache PROJECT_NAME

== First Slide
```

### Rule 4: Use ONLY == for Slides

Every slide MUST use `==` (level 2 heading). 

- `==` = a new slide ✅
- `===` = a vertical sub-slide (DO NOT USE — they don't render properly) ❌
- `=` = document title/preamble (DO NOT USE) ❌

### Rule 5: Content Limits Per Slide

These are HARD LIMITS. Violating them causes text to overflow off-screen:

| Element | Maximum |
|---------|---------|
| Bullet points | 4–5 |
| Table rows (data) | 4–5 |
| Code block lines | 6–8 |
| Total visible text lines | 6–7 |

If you have more content, SPLIT into multiple slides with clear titles.

### Rule 6: Never Combine Bullets + Large Image

If a slide has an image AND more than 2 bullet points, split it:
- Slide A: the explanation bullets
- Slide B: the image with a brief caption

### Rule 7: Never Name the Project Chair

Apache is about community, not individuals. The PMC Chair role rotates.
Do not include the name of the current chair anywhere in the presentation.
You may explain the PMC Chair *role* generically in the governance section.

### Rule 8: Speaker Notes

Add `[.notes]` blocks for instructor context. These don't appear on screen:

```asciidoc
[.notes]
--
Explain why this matters. Mention common misconceptions.
Suggest a demo at this point in the presentation.
--
```

### Rule 9: Three-Part Structure

Target ~25 slides total, organized as:

**Part 1: What Is It? (~8 slides)**
- Title slide (logo + tagline)
- What is it? (elevator pitch, 3-4 bullets)
- Problem it solves / why it exists
- Key features (4-5 bullets max)
- Architecture overview (brief, not a diagram dump)
- Use cases (3-4 with examples)
- Project vitals (PMC size, contributor count, established year — NO chair name)

**Part 2: Installation & Getting Started (~8 slides)**
- Prerequisites (OS, language, runtime)
- Install methods (one slide per method, keep commands to 4-6 lines)
- Hello World (simplest possible working example)
- Configuration basics (3-4 key settings)
- Next steps / where to go deeper

**Part 3: Community Participation (~7 slides)**
- Communication channels (mailing lists, chat, GitHub — bullets not tables)
- How to contribute (5 steps max)
- Types of contributions (code, docs, testing, support — 4-5 bullets)
- Governance roles (User → Contributor → Committer → PMC, explained briefly)
- Resources & links (4-5 bullets max)
- Thank you / Q&A slide

### Rule 10: Code Blocks

Use `[source,language]` blocks:

```asciidoc
[source,bash]
----
./bin/start.sh
curl http://localhost:8080/health
----
```

Keep code blocks to 6-8 lines MAX. If a real example is longer, show only
the essential lines with comments indicating what's omitted.

### Rule 11: Slide Title Style

- Keep titles short (3-5 words)
- Use sentence case, not UPPERCASE
- Be specific: "Install with Docker" not "Installation Method 2"

### Rule 12: Image References

For the title slide, reference the local project logo:
```asciidoc
image::project-logo.png[Apache PROJECT_NAME, 500]
```

For architecture diagrams or screenshots, use external URLs if stable:
```asciidoc
image::https://project.apache.org/img/architecture.png[width=70%]
```

Keep image width to 70% max to leave room for the fixed logos.

## Build & Verify

After generating all files:

```bash
cd content/Apache/ProjectName
rm -rf target .asciidoctor
../../../mvnw process-resources -Drat.skip=true
open target/generated-slides/index.html
```

## Common Mistakes to Avoid

1. **Using `===` instead of `==`** → slides won't render as separate pages
2. **Content before first `==`** → persistent overlay on every slide
3. **Using `= Title`** → creates document preamble, same problem
4. **More than 5 bullets** → text overflows off bottom of screen
5. **Code blocks > 8 lines** → overflows
6. **Naming the project chair** → individuals change; Apache is community-first
7. **Adding `:revealjsdir:` in the adoc** → conflicts with Maven build
8. **Tables with 6+ rows** → overflow
9. **Bullets + image on same slide** → overflow
10. **Referencing `project-logo.svg`** → the file is `.png` (from apache.org/logos)
