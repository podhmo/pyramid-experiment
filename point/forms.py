import wtforms.form as form
import wtforms.fields as fields
import wtforms.validators as validators

class PointForm(form.Form):
    x = fields.IntegerField(label="x", validators=[validators.Required()])
    y = fields.IntegerField(label="y", validators=[validators.Required()])
    name = fields.TextField(label="name", validators=[validators.Required()])


