<%inherit file="../base.mako"/>
<%namespace name="co" file="../components.mako"/>

<%block name="content">
  <a href="${request.route_path("point_create")}">create</a>
  <form action="${request.route_path("point_create")}" method="POST">
    <table>
      <thead>
        <tr>
          <th>name</th>
          <th>x</th>
          <th>y</th>
        </tr>
      </thead>
      <tbody>
    % for p in points:
      <tr>
        ##<td><a href="${request.route_path("point_view", id=point.id)"></td>
        <td><a href="#">${p.name}</a></td>
        <td>${p.x}</td>
        <td>${p.y}</td>
      </tr>
    % endfor
      </tbody>
    </table>
  </form>
</%block>
