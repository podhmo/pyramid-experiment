<%inherit file="../base.mako"/>
<%namespace name="co" file="../components.mako"/>

<%block name="content">
  <form action="${request.route_path("point_create")}" method="POST">
    <table>
    ${co.tr_field(form, "name")}
    ${co.tr_field(form, "x")}
    ${co.tr_field(form, "y")}
    <input type="hidden" name="stage" value="${stage}"/>
    <button type="submit">submit</button>
    </table>
  </form>
</%block>
