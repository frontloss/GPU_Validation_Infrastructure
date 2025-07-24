<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" />
  <xsl:template match="/">
    <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"&gt;</xsl:text>
    <html>
      <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>
          GfxDisplay Automation Test Execution Log of::
          <xsl:value-of select="/ExecutionLog/Summary/TestName" />
        </title>
        <style type="text/css">
          body
          {
          margin: 0;
          padding: 0;
          font-family: Tahoma, Sans-Serif;
          }
          table
          {
          width: 100%;
          }
          #center
          {
          width: 745px;
          margin: 0 auto;
          }
          #header
          {
          position: fixed;
          top: 0;
          width: 745px;
          background-color: #0065B6;
          }
          #logHeader
          {
          position: fixed;
          width: 745px;
          padding-top: 90px;
          border-bottom: 2px solid white;
          font-weight: bold;
          }
          #container
          {
          overflow: auto;
          padding-top: 100px;
          width: 745px;
          font-size: small;
          }
          #footer
          {
          position: fixed;
          bottom: 0;
          width: 745px;
          border-top: 2px solid white;
          background-color: #0065B6;
          }
          .arrow
          {
          width: 3%;
          padding-top: 3px;
          padding-bottom: 5px;
          border-bottom: 1px solid #F0F0F0;
          }
          .timeStamp
          {
          width: 27%;
          padding-top: 3px;
          padding-bottom: 5px;
          border-bottom: 1px solid #F0F0F0;
          }
          .ParenttimeStamp
          {
          width: 27%;
          padding-top: 3px;
          padding-bottom: 5px;
          border-bottom: 1px solid #F0F0F0;
          }
          .ChildtimeStamp
          {
          width: 27%;
          padding-top: 3px;
          padding-bottom: 5px;
          border-bottom: 1px solid #F0F0F0;
          padding-left: 20px;
          }
          .log
          {
          width: 70%;
          padding-top: 3px;
          padding-bottom: 5px;
          border-bottom: 1px solid #F0F0F0;
          }
          .Parent
          {
          cursor:pointer;
          background-color: #AAFFAA;
          }
          .Child
          {
          padding-left: 3px;
          }
        </style>
        <script type="text/javascript" src="Toggler.js">
          <![CDATA[
            window.onbeforeunload = function () {
            }
          ]]>
        </script>
      </head>
      <body>
        <div id="center">
          <div id="header">
            <table>
              <tr>
                <td style="width: 90%; color: White;" align="right">
                  <table style="width: 100%;">
                    <tr>
                      <td style="width: 5%; font-size:0.7em; text-align: right; vertical-align:bottom;">TestName</td>
                      <td style="width: 95%; text-align: left; font-weight:bold;">
                        <xsl:value-of select="/ExecutionLog/Summary/TestName" />
                      </td>
                    </tr>
                    <tr>
                      <td style="width: 5%; font-size:0.7em; text-align: right; vertical-align:bottom;">RunTime</td>
                      <td style="width: 95%; text-align: left; font-weight:bold; font-size:0.7em;">
                        <xsl:value-of select="/ExecutionLog/Summary/Breakup/RunTime" />
                      </td>
                    </tr>
                    <tr>
                      <td style="width: 5%; font-size:0.7em; text-align: right; vertical-align:bottom;">Result</td>
                      <td style="width: 95%; text-align: left; font-weight:bolder; vertical-align:bottom;">
                        <xsl:if test="/ExecutionLog/Summary/Result='PASSED'">
                          <font style="background:Green; color:White; padding: 3px 5px 3px 5px ;">
                            <xsl:value-of select="/ExecutionLog/Summary/Result" />
                          </font>
                        </xsl:if>
                        <xsl:if test="/ExecutionLog/Summary/Result='FAILED'">
                          <font style="background:#FF3300; color:White; padding: 3px 5px 3px 5px ;">
                            <xsl:value-of select="/ExecutionLog/Summary/Result" />
                            <xsl:if test="/ExecutionLog/Summary/Breakup/FirstFailMsg!=''">
                              &#160;:&#160;
                              <xsl:if test="string-length(/ExecutionLog/Summary/Breakup/FirstFailMsg)>49">
                                <font style="font-size:0.7em; font-weight:bold;">
                                  <xsl:value-of select="/ExecutionLog/Summary/Breakup/FirstFailMsg" />
                                </font>
                              </xsl:if>
                              <xsl:if test="not(string-length(/ExecutionLog/Summary/Breakup/FirstFailMsg)>49)">
                                  <xsl:value-of select="/ExecutionLog/Summary/Breakup/FirstFailMsg" />
                              </xsl:if>
                            </xsl:if>
                          </font>
                        </xsl:if>
                        <xsl:if test="/ExecutionLog/Summary/Result='CUSTOM'">
                          <font style="background:Blue; color:White; padding: 3px 5px 3px 5px ;">
                            <xsl:value-of select="/ExecutionLog/Summary/Result" />
                          </font>
                        </xsl:if>
                      </td>
                    </tr>
                    <tr>
                      <td style="width: 100%; text-align: left; vertical-align:bottom;" colspan="2">
                        &#160;
                        <xsl:if test="/ExecutionLog/Summary/Breakup/Sporadic!='0'">
                          <font style="font-size:0.7em; font-weight:bold; color:Magenta; padding: 1px 3px 1px 3px;">
                            Sporadicness Observed
                          </font>
                        </xsl:if>
                      </td>
                    </tr>
                  </table>
                </td>
                <td style="width: 10%; text-align: left; vertical-align:center; padding-bottom: 5px;">
                  <img src="./Intel_logo.jpg" alt="Intel Corp" />
                </td>
              </tr>
            </table>
          </div>
          <div id="logHeader">
            <table style="background-color: #B4D2EF; color: #0065B6;">
              <tr>
                <td style="width: 30%">
                  Timestamp
                </td>
                <td style="width: 70%">
                  Log
                </td>
              </tr>
            </table>
          </div>
          <div id="container">
            <table id="tblContainer" cellspacing="0">
              <xsl:for-each select="/ExecutionLog/Report/Log">
                <xsl:if test="Transformable='true'">
                  <tr id="{Id}" class="{Level}"  type="{Type}" error="{Error}">
                    <td class="arrow">
                      <xsl:if test="Level='Parent'">
                        &#9658;
                      </xsl:if>
                      <xsl:if test="Level='Child'">
                        &#160;
                      </xsl:if>
                    </td>
                    <td class="{Level}timeStamp">
                      <xsl:value-of select="Timestamp" />
                    </td>
                    <td class="log">
                      <table width="100%">
                        <tr>
                          <td>
                            <xsl:value-of select="Data" disable-output-escaping="yes" />
                          </td>
                        </tr>
                        <xsl:if test="Screenshot">
                          <tr>
                            <td>
                              <a href="{Screenshot}">
                                <img style="border: 0; width: 30%; height: 30%" src="{Preview}" alt="Error Snapshot" />
                              </a>
                            </td>
                          </tr>
                        </xsl:if>
                      </table>
                    </td>
                  </tr>
                </xsl:if>
              </xsl:for-each>
            </table>
          </div>
          <div id="footer">
            <table style="font-size: x-small; color: White;">
              <tr>
                <td style="width: 50%; text-align: left;">
                  Display Automation Test Execution Log
                </td>
                <td style="width: 50%; text-align: right;">
                  &#169; Intel Corporation
                </td>
              </tr>
            </table>
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>