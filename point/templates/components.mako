<%def name="tr_field(form, k)">
  <tr><th>${getattr(form,k).label}</th><td>${getattr(form,k)}
      % if k in form.errors:
        <br/>
        % for error in form.errors[k]:
          <span class="btn btn-danger">${error}</span>
        % endfor
      % endif
  </td></tr>
</%def>
