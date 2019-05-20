An asciidoctor block macro to render mxgraph blocks
===================================================

## Purpose
This blockprocessor converts an xml representation of an [mxGraph](https://github.com/jgraph/mxgraph) into an image that is then passed on to asciidoctorj as an image block.

There are multiple ways of creating mxgraphs, one of the most prominents ones is [draw.io](https://draw.io) .

## Usage

### Defining Blocks in Asciidoctor
By marking literal blocks as _drawio_ this processor gets called and renders the content of that block.
The second block parameter is used as the file name for the generated image.
```
[drawio,testdrawdiag]
....
include::diagrams/drawiotest.xml[]
....
```

Any extra parameters passed to the block are handed through to the asciidoctor backend that is configured to allow for further customization.

```
[drawio,testdrawdiag2,float="right",align="middle"]
....
<?xml version="1.0" encoding="UTF-8"?><mxGraphModel dx="2086" dy="1271" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1"
              page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <mxCell id="L3S7H67dfCK0_i4HHWqK-3"
            style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1"
            source="L3S7H67dfCK0_i4HHWqK-1" target="L3S7H67dfCK0_i4HHWqK-2">
      <mxGeometry relative="1" as="geometry"/>
    </mxCell>
    <mxCell id="L3S7H67dfCK0_i4HHWqK-1" value="Hallo" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="120" y="260" width="120" height="60" as="geometry"/>
    </mxCell>
    <mxCell id="L3S7H67dfCK0_i4HHWqK-2" value="Hallo2" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
      <mxGeometry x="450" y="260" width="120" height="60" as="geometry"/>
    </mxCell>
  </root>
</mxGraphModel>
....
```

### Configuration
The processor takes some configuration options.
The following options can either be defined at the document level or at block level, with those defined at block level overriding the document variables.

| Parameter   | Description                                                 | Scope            | Default |
|:------------|:------------------------------------------------------------|:-----------------|:--------|
| basedir     | Base directory, relative to which other paths are resolved. | Document / Block | ""      |
| imagedir    | Directory that images are generated in.                     | Document / Block | images  |
| imageformat | Format for images.                                          | Document / Block | png     |
| alttext     | Hover text for image.                                       | Block            | ""      |
| titletext   | Title text.                                                 | Block            | ""      |

### Passing variables from Maven
When using the Maven AsciidoctorJ module, attributes defined in the pom file can be used in the document like regular variables.


## Next steps
This is currently a very early version of this processor. It works and generates simple graphs well enough, but for more complex graphs there are issues with spacing and some block formating not showing up correctly.
I will look at this in the upcoming weeks.