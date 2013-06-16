<#include "resources/filters/header.ftl"/>
<div id="content">
<table>
<thead>
<tr><th>URI</th><th>Operations</th><th>Description</th><th>Arguments</th></tr>
</thead>
<tbody>
<tr class="even"><td><a href="${root}version">/version</a></td><td>GET</td><td>Software version number</td><td></td></tr>
<tr class="odd"><td><a href="${root}analyzer/html">/analyzer/html</a></td><td>GET</td><td>Statistics describing analyzer performance</td><td></td></tr>
<tr class="even"><td><a href="${root}analyzer/json">/analyzer/json</a></td><td>GET</td><td>Statistics describing analyzer performance</td><td></td></tr>
<tr class="odd"><td><a href="${root}agents/html">/agents/html</a></td><td>GET</td><td>List agents</td><td></td></tr>
<tr class="even"><td><a href="${root}agents/json">/agents/json</a></td><td>GET</td><td>List agents</td><td></td></tr>
<tr class="odd"><td><a href="${root}metrics/html">/metrics/html</a></td><td>GET</td><td>List currently active metrics</td><td></td></tr>
<tr class="even"><td><a href="${root}metrics/json">/metrics/json</a></td><td>GET</td><td>List currently active metrics</td><td></td></tr>
<tr class="odd"><td>/metric/{agent}/html</td><td>GET</td><td>Retrieve metrics for agent</td><td>accepts same arguments as json query below</td></tr>
<tr class="even"><td>/metric/{agent}/json</td><td>GET</td><td>Retrieve metrics for agent</td><td><b>agent:</b> ip address or hostname of agent</td></tr>
<tr class="odd"><td>/metric/{agent}/{metric}/html</td><td>GET</td><td>Plot metric</td><td>accepts same arguments as json query below</td></tr>
<tr class="even"><td>/metric/{agent}/{metric}/json</td><td>GET</td><td>Retrieve metric</td><td><b>agent:</b> list of agent addresses/hostnames e.g. 10.0.0.1;switch1 - the token <i>ALL</i> represents all agents<br /><b>metric:</b> ordered list of metric names, e.g. load_one,load_five - prefix metric with <i>max:</i>, <i>min:</i>, <i>sum:</i>, <i>avg:</i>, <i>var:</i>, <i>sdev:</i>, <i>med:</i>, <i>q1:</i>, <i>q2:</i>, <i>q3:</i>, <i>iqr:</i> or <i>any:</i> to specify aggregation operation, e.g. max:load_one,min:load_one.
Default aggregation <i>max</i> is used if no prefix specified<br />
<b>query:</b> query parameters applied as filter to select agents based on metrics, e.g. os_name=linux,windows&cpu_num=2&hostname=*web.*</b></td></tr>
<tr class="odd"><td>/dump/{agent}/{metric}/html</td><td>GET</td><td>Dump metric values</td><td>accepts same arguments as json query below</td></tr>
<tr class="even"><td>/dump/{agent}/{metric}/json</td><td>GET</td><td>Dump metric values</td><td><b>agent:</b> list of agent addresses/hostnames e.g. 10.0.0.1;switch1 - the token <i>ALL</i> represents all agents<br /><b>metric:</b>list of metric names, e.g. load_one;load_five - the token <i>ALL</i> represents all metrics<br /><b>query:</b> query parameters applied as filter to select agents based on metrics, e.g. os_name=linux,windows&cpu_num=2&hostname=*web.*</b></td></tr>
<tr class="odd"><td><a href="${root}flowkeys/html">/flowkeys/html</a></td><td>GET</td><td>List currently active flow keys</td><td></td></tr>
<tr class="even"><td><a href="${root}flowkeys/json">/flowkeys/json</a></td><td>GET</td><td>List currently active flow keys</td><td></td></tr>
<tr class="odd"><td><a href="${root}flow/html">/flow/html</a></td><td>GET, POST</td><td>Manage flow definitions</td><td><b>name:</b> name used to identify flow specification<br/><b>keys:</b> list of flowkey attributes, e.g. ipsource,ipdestination<br /><b>value:</b> <i>frames</i> or <i>bytes</i><br /><b>filter:</b> boolean expression filtering flowkeys, e.g. sourcegroup=local&destinationgroup=external</td></tr>
<tr class="even"><td><a href="${root}flow/json">/flow/json</a></td><td>GET</td><td>List flow definitions</td><td></td></tr>
<tr class="odd"><td>/flow/{name}/json</td><td>GET, PUT, DELETE</td><td>Manage flow definition</td><td><b>name:</b> name used to identify flow specification<br />Flow parameters are expressed as JSON object, e.g. {keys:'ipsource,ipdestination', value:'bytes', filter:'ipprotocol=1'}</td></tr>
<tr class="even"><td><a href="${root}group/json">/group/json</a></td><td>PUT, GET</td><td>Manage IP address groups</td><td>Groups define <i>sourcegroup</i>, <i>destinationgroup</i> attributes for flows, e.g. {external:['0.0.0.0/0'], internal:['10.0.0.0/8','172.16.0.0/12','192.168.0.0/16']}</td></tr>
<tr class="odd"><td><a href="${root}threshold/html">/threshold/html</a></td><td>GET, POST</td><td>Manage thresholds</td><td><b>name:</b> name used to identify threshold specification<br/><b>metric:</b> metric to apply threshold to, e.g. load_one<br/><b>value:</b> threshold value, e.g. 1.0<br/><b>filter:</b> query encoded filter expression consistent with metric query, e.g. os_name=linux&cpu_num=2</td></tr>
<tr class="even"><td><a href="${root}threshold/json">/threshold/json</a></td><td>GET</td><td>Retrieve thresholds</td><td></tr></tr>
<tr class="odd"><td>/threshold/{name}/json</td><td>GET, PUT, DELETE</td><td>Manage definition of threshold</td><td><b>name:</b> name used to identify threshold specification<br />Threshold parameters are expressed as JSON object, e.g. {metric:"load_one", value:1, filter:{os_name:["linux"]}}</td></tr>
<tr class="even"><td><a href="${root}events/html">/events/html</a></td><td>GET</td><td>List events</td><td></td></tr>
<tr class="odd"><td><a href="${root}events/json">/events/json</a></td><td>GET</td><td>List events</td><td><b>query:</b> Used to block for events, e.g. ?eventID=10&maxEvents=10&timeout=60, waits for up to 60 seconds for events after eventID 10</td></tr>
</tbody>
</table>
<p><b>Note:</b> REST API is not final and is subject to change in future releases.</p>
</div>
<#include "resources/filters/footer.ftl">
