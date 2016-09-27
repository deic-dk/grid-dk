<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:zi="http://zero-install.sourceforge.net/2004/injector/interface"
		version="1.0">

  <xsl:output method="xml" encoding="utf-8"
	doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
	doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>

  <xsl:template match="/zi:interface">
    <html>
      <head>
        <title>
          <xsl:value-of select="zi:name"/>
        </title>
	<style type='text/css'>
	  html { background: #d0d0ff; }
	  body { background: #d0d0ff; margin: 0; padding: 0; color: black;}
	  h1 { text-align: center; border-bottom: 2px solid #d0d0ff; padding-bottom: .5em; }
	  div.main { padding: 1em; background: white;
	  	    -moz-border-radius: 1em 1em 1em 1em; max-width: 60em;
		    margin-left: auto; margin-right: auto;
		    margin-top: 1em; margin-bottom: 1em;}
	  dt { font-weight: bold; text-transform:capitalize; }
	  dd { padding-bottom: 1em; }
	  dl.group { margin: 0.5em; padding: 0.5em; border: 1px dashed #888;}
	  dl.impl { padding: 0.2em 1em 0.2em 1em; margin: 0.5em; border: 1px solid black; background: white;}
	  pre { background: #ddd; color: black; padding: 0.2cm; }
	  table { width: 100%% }
	  th { background: #d0d0ff; text-align: left; }
	  td { background: #e0e0ff; text-align: left; }
	</style>
      </head>
      <body>
       <div class='main'>
        <h1><xsl:value-of select="zi:name"/> - <xsl:value-of select='zi:summary'/></h1>

	<dl>

	  <xsl:apply-templates mode='dl' select='*|@*'/>

	  <xsl:choose>
	    <xsl:when test='//zi:package'>
	    <dt>Available Packages</dt>
	    <dd>
	      <p>The list below contains references to all matching packages.
	      </p>
	      <table>
	       <tr><th>Package</th></tr>
	       <xsl:for-each select='//zi:package'>
	        <tr>
	         <td>
	           <a href='{@href}'><xsl:value-of select='@name'/></a>
	         </td>
	        </tr>
	       </xsl:for-each>
	      </table>
	    </dd>
	    </xsl:when>
	  </xsl:choose>
	</dl>
	<dt>Available Actions</dt>
	<dd>
	  <p>
	    Search for packages (enter prefix or wildcard pattern):
	    <form action='%(document_root)s/package' method='get'>
	      <table>
		<tr><td>Pattern</td></tr>
		<tr><td><input type='text' name='pattern'/></td></tr>
		<tr><td><input type='submit' value='Search'/></td></tr>
	      </table>
	    </form>
	  </p>
	  <p>
	    Edit packages
	    <form action='%(document_root)s/package' method='post'>
	      <table>
		<tr><td>Package</td><td colspan='2'>Source</td><td>Owner</td></tr>
		<tr>
		  <td><input type='text' size='20%%' name='package'/></td>
		  <td colspan='2'><input type='text' size='30%%' name='source'/></td>
		  <td><input type='text' size='20%%' name='owner'/></td>
		</tr>
		<tr>
		  <td colspan='4'><input type='submit' value='Save'/></td>
		</tr>
	      </table>
	    </form>
	  </p>
	</dd>
       </div>
      </body>
    </html>
  </xsl:template>
  
  <xsl:template mode='dl' match='/zi:interface/@uri'>
    <dt>Address</dt><dd><p><a href='%(document_root)s{.}'>%(document_root)s<xsl:value-of select="."/></a></p></dd>
  </xsl:template>

  <xsl:template mode='dl' match='zi:description'>
    <dt>Description</dt><dd><p><xsl:value-of select="."/></p></dd>
  </xsl:template>

  <xsl:template mode='dl' match='zi:icon'>
    <dt>Icon</dt><dd><p><img src='{@href}'/></p></dd>
  </xsl:template>

  <xsl:template mode='dl' match='*|@*'/>

  <xsl:template match='zi:package'>
    <dl class='impl'>
      <xsl:apply-templates mode='attribs' select='@stability|@version|@id|@arch|@released'/>
      <xsl:apply-templates/>
    </dl>
  </xsl:template>

  <xsl:template mode='dl' match='zi:search'>
    <dt>Search Status</dt><dd><p>Searching for packages matching
    pattern '<xsl:value-of select="."/>'</p></dd>
  </xsl:template>

  <xsl:template mode='dl' match='zi:edit'>
    <dt>Edit Status</dt><dd><p><xsl:value-of select="."/></p></dd>
  </xsl:template>

  <xsl:template mode='attribs' match='@*'>
    <dt><xsl:value-of select='name(.)'/></dt>
    <dd><xsl:value-of select='.'/></dd>
  </xsl:template>

</xsl:stylesheet>
