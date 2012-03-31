import wtforms.form as form
import wtforms.fields as fields
import wtforms.validators as validators

class PointForm(form.Form):
    x = fields.IntegerField(label="x")
    y = fields.IntegerField(label="y")
    name = fields.TextField(label="name", validators=[validators.Required()])


