<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="text" />
  <xsl:template name="fnPad">
    <xsl:param name="argString" select="'@'"/>
    <xsl:param name="argLength" select="80"/>
    <xsl:value-of select="$argString"/>
    <xsl:if  test="$argLength&gt;1">
      <xsl:call-template name="fnPad">
        <xsl:with-param name="argLength" select="number($argLength) - 1"/>
        <xsl:with-param name="argString" select="$argString"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
  <xsl:template match="/">
    <xsl:call-template name="fnPad" />
    <xsl:text>&#xa;</xsl:text>
    <xsl:text xml:space="preserve"># Total Pass: </xsl:text>
    <xsl:value-of select="/ExecutionLog/Summary/Breakup/Pass" />
    <xsl:text>&#xa;</xsl:text>
    <xsl:text xml:space="preserve"># Total Fail: </xsl:text>
    <xsl:value-of select="/ExecutionLog/Summary/Breakup/Fail" />
    <xsl:text>&#xa;</xsl:text>
    <xsl:text xml:space="preserve"># Total Sporadic: </xsl:text>
    <xsl:value-of select="/ExecutionLog/Summary/Breakup/Sporadic" />
    <xsl:text>&#xa;</xsl:text>
    <xsl:call-template name="fnPad" />
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:call-template name="fnPad">
      <xsl:with-param name="argString" select="'*'"/>
      <xsl:with-param name="argLength" select="15"/>
    </xsl:call-template>
    <xsl:text xml:space="preserve">T E S T&#9;</xsl:text>
    <xsl:value-of select="/ExecutionLog/Summary/Result" />
    <xsl:call-template name="fnPad">
      <xsl:with-param name="argString" select="'*'"/>
      <xsl:with-param name="argLength" select="15"/>
    </xsl:call-template>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text xml:space="preserve">Detailed log can be found at: </xsl:text>
    <xsl:value-of select="/ExecutionLog/Summary/TestName" />
    <xsl:text>.xml</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:call-template name="fnPad" />
  </xsl:template>
</xsl:stylesheet>