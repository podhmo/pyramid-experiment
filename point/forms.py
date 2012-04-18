import wtforms.form as form
import wtforms.fields as fields
import wtforms.validators as validators

# @render_config(kind="input", renderer="input.mako", displays=["name", "x", "y"])
# @render_config(kind="output", renderer="output.mako", displays=["name", "x", "y"])
class PointForm(form.Form):
    x = fields.IntegerField(label="x", validators=[validators.Required()])
    y = fields.IntegerField(label="y", validators=[validators.Required()])
    name = fields.TextField(label="name", validators=[validators.Required()])

if __name__ == "__main__":
    form = PointForm()
    print form.meta.display_fields
    form.meta.hey()
    print [(k, type(v)) for k, v in form.__dict__.items() if isinstance(v, fields.Field)]
 
