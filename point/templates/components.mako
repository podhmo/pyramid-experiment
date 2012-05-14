<%def name="form_to_table(form)">
<table class="table table-striped">
  <tbody>
  % for k,v in form.data.iteritems():
    <tr>
	  <td>${getattr(form,k).label}</td>
	  <td>${v}</td>
	</tr>
  % endfor
  </tbody>
</table>
</%def>

<%def name="form_as_table_strict(form, keys)">
<table class="table table-striped">
  <tbody>
  % for k in keys:
    ${tr_field(form, k)}
  % endfor
  </tbody>
</table>
</%def>

<%def name="label_with_required_mark(field)">
  %if field.flags.required:
    <%
      field.label.text += "*"
     %>
  %endif

 ${field.label}
</%def>

<%def name="tr_field(form, k)">
    <%
      field = getattr(form,k)
    %>

	<tr><th>${label_with_required_mark(field)}</th><td>${field}
	%if k in form.errors:
	  <br/>
	  %for error in form.errors[k]:
		<span class="btn btn-danger">${error}</span>
	  %endfor
	%endif
	</td></tr>
</%def>

<%def name="post_to_hidden_inputs(post)">
  % for k, v in post.items():
    <input type="hidden" name="${k}" value="${v}"/>
  % endfor
</%def>
