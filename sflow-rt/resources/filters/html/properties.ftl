<#include "resources/filters/header.ftl"/>
<div id="content">
<h1>System Properties</h1>
<p>The following System properties can be set in the <b>start.sh</b> or <b>start.bat</b> script:</p>
<table>
<thead>
<tr><th>Poperty</th><th>Default</th><th>Description</th></tr></thead>
</thead>
<tbody>
<tr class="odd"><td>http.port</td><td>8008</td><td>TCP port to receive HTTP requests</td></tr>
<tr class="even"><td>http.log</td><td>no</td><td>Set to <i>yes</i> to enable http request logging</td></tr>
<tr class="odd"><td>sflow.port</td><td>6343</td><td>UDP port to receive sFlow</t
d></tr>
<tr class="even"><td>sflow.file</td><td></td><td>Playback sFlow from pcap file (disables <i>sflow.port</i>)</td></tr>
<tr class="odd"><td>events.max</td><td>1000</td><td>Maximum number of events to keep</td></tr>
</tbody>
</table>
</div>
<#include "resources/filters/footer.ftl">
