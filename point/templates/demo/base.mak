<!DOCTYPE html>
<html>
  <%
  from js.bootstrap import bootstrap
  bootstrap.need()
  %>
  <head>
    <%block name="with_head" />
  </head>
  <body>
    <div class="navigator">
      <div class="navigator-inner">
        <div class="container">
          ${next.body()}
        </div>
      </div>
    </div>
  </body>
</html>
