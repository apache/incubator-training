package org.apache.training.drawioprocessor;

import org.asciidoctor.Asciidoctor;
import org.asciidoctor.extension.JavaExtensionRegistry;
import org.asciidoctor.jruby.extension.spi.ExtensionRegistry;

public class DrawioExtension implements ExtensionRegistry {

  @Override
  public void register(Asciidoctor asciidoctor) {
    final JavaExtensionRegistry javaExtensionRegistry = asciidoctor.javaExtensionRegistry();
    javaExtensionRegistry.block("drawio", new DrawioBlockProcessor("drawio", null) );

  }
}
