package org.apache.training.drawioprocessor;

import static org.apache.training.drawioprocessor.DrawioProcessorConfig.ALT_TEXT_CONFIG;
import static org.apache.training.drawioprocessor.DrawioProcessorConfig.BASE_PATH_CONFIG;
import static org.apache.training.drawioprocessor.DrawioProcessorConfig.IMAGE_FORMAT_CONFIG;
import static org.apache.training.drawioprocessor.DrawioProcessorConfig.IMAGE_PATH_CONFIG;
import static org.apache.training.drawioprocessor.DrawioProcessorConfig.TITLE_CONFIG;

import com.mxgraph.io.mxCodec;
import com.mxgraph.util.mxCellRenderer;
import com.mxgraph.util.mxXmlUtils;
import com.mxgraph.view.mxGraph;
import java.awt.*;
import java.awt.image.RenderedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.imageio.ImageIO;
import org.asciidoctor.ast.StructuralNode;
import org.asciidoctor.extension.BlockProcessor;
import org.asciidoctor.extension.Name;
import org.asciidoctor.extension.Reader;
import org.w3c.dom.Document;

@Name("drawio")
public class DrawioBlockProcessor extends BlockProcessor {
  // These default values will be used unless specified otherwise in the block attributes
  private static final String DEFAULT_IMAGE_PATH = "images/";
  private static final String DEFAULT_IMAGE_FORMAT = "png";

  private mxGraph graph = new mxGraph();
  private String fileName = "";
  private String basePath = "";
  private String imagePath = "";
  private String altText = "";
  private String title = "";
  private String imageFormat = "";

  public DrawioBlockProcessor(String name, Map<String, Object> config) {
    super(name, createConfig());
  }

  @Override
  public Object process(StructuralNode parent, Reader reader, Map<String, Object> attributes) {
    graph.setHtmlLabels(true);
    StringBuilder blockContent = new StringBuilder();
    List<String> lines = reader.readLines();
    for (String line : lines) {
      blockContent.append(line);
    }

    Document doc = mxXmlUtils.parseXml(blockContent.toString());
    mxCodec codec = new mxCodec(doc);
    codec.decode(doc.getDocumentElement(), graph.getModel());
    RenderedImage image = mxCellRenderer.createBufferedImage(graph, null, 1,
        Color.WHITE, false, null);


    initialize(parent.getDocument().getAttributes(), attributes);

    try {
      ImageIO.write(image, imageFormat, new File(basePath + imagePath + fileName));
    } catch (IOException e) {
      e.printStackTrace();
    }

    final HashMap<String, Object> attrs = new HashMap<String, Object>();

    attributes.put("target", fileName);
    attributes.put("alt", altText);
    attributes.put("title", title);
    return createBlock(parent, "image", "", attributes, new HashMap<Object, Object>());
  }


  private void initialize(Map<String, Object> documentAttributes, Map<String, Object> blockAttributes) {
    // Obtain config values, priority is as follows (lower number beats higher number):
    // 1. attributes specified in block definition
    // 2. attributes set at document level
    // 3. default values

    // base path, image path will be resolved relative tho this path
    basePath = ensureTrailingSlash(getAttribute(blockAttributes, documentAttributes, BASE_PATH_CONFIG, ""));

    // directory name in which images are generated (relative to basePath)
    imagePath = ensureTrailingSlash(getAttribute(blockAttributes, documentAttributes, IMAGE_PATH_CONFIG, DEFAULT_IMAGE_PATH));
    ensureTrailingSlash(imagePath);

    // hover text for image
    altText = getAttribute(blockAttributes, documentAttributes, ALT_TEXT_CONFIG, "");

    // title to show for image on slide
    title = getAttribute(blockAttributes, documentAttributes, TITLE_CONFIG, "");

    // imageformat (png, jpg, ...)
    imageFormat = getAttribute(blockAttributes, documentAttributes, IMAGE_FORMAT_CONFIG, DEFAULT_IMAGE_FORMAT);

    // filename, cannot be retrieved from attributes of document, this has to come from
    // the block definition and is a positional argument
    fileName = (String)blockAttributes.get("2") + "." + imageFormat;
  }

  private String getAttribute(Map<String, Object> primaryAttributes, Map<String, Object> secondaryAttributes, String key, String defaultValue) {
    String result = "";
    try {
      result = (String)primaryAttributes.getOrDefault(key, getAttribute(secondaryAttributes, key, defaultValue));
    } catch (Exception e) {
      System.out.println("Warning: Couldn't cast value for attribute key '" + key + "' to String, falling back to default value: '" + defaultValue + "'");
    }
    return result;
  }


    private String getAttribute(Map<String, Object> attributes, String key, String defaultValue) {
    String result = defaultValue;
    try {
      result = (String) attributes.getOrDefault(key, defaultValue);
    } catch (Exception e) {
      System.out.println("Warning: Couldn't cast value for attribute key '" + key + "' to String, falling back to default value: '" + defaultValue + "'");
    }
    return result;


  }

  private String ensureTrailingSlash(String path) {
     return path.endsWith("/") ? path : path + "/";
  }

  private static Map<String, Object> createConfig() {
    Map<String, Object> result = new HashMap<>();
    result.put("contexts", createContextsConfig());
    return result;
  }

  private static List<String> createContextsConfig() {
    List<String> contexts = new ArrayList<>();
    contexts.add(":literal");
    return contexts;
  }
}
