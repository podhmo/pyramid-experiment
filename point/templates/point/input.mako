<%namespace name="co" file="../components.mako"/>

<form action="${request.next_flow_path}" method="POST">
${co.form_as_table_strict(form, form.data.keys())}
<input type="submit"/>
</form>
