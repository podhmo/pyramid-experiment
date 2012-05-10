<%inherit file="../base.mako"/>
<%namespace name="co" file="../components.mako"/>

<%block name="content">
<div>
  <h1>confirm</h1>
  <ul>
    <li>name: ${form.data["name"]}</li>
    <li>x: ${form.data["x"]}</li>
    <li>y: ${form.data["y"]}</li>
  <ul>
</div>

  <form action="${request.route_path("point_create")}" method="POST">
    <table>
    ${co.post_to_hidden_inputs(request.POST)}
    <input type="hidden" name="stage" value="${stage}"/>
    <button type="submit">submit</button>
    </table>
  </form>
</%block>
