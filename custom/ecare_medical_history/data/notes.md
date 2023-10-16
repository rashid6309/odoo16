<h1>Patient Timeline </h1>
<li>Timeline record only created by action "Create Patient Timeline" button in the header</li>
<li>Timeline record can't be deleted</li>
<li>Unique constraint is applied at DB</li>

<h3> Banner Route</h3>
To use Banner route in any-model we need field of "ec.medical.patient" and then we can use widget over that. 

<h3> Obstetrics</h3>
Anywhere the obstetrics is shown all of its records are visible. 
order by create date desc.

<h3>Previous Treatment</h3>
Anywhere the previous treatments is shown all of its records are visible. 
order by create date desc.

<h2>Repeat Consultation </h2>
<li>Unique constraint is applied at DB</li>
<h3> Factors </h3>
Factor edit button which was initially decided was actually discarded for now, below is the code needed to be used in case:
Under Male Factor
<button class="factor-action-button p-0"
        type="object"
        name="action_create_repeat_consultation">
    <div class="factor-action-button">
        <div class="factor-icon">
            <i title="Edit" class="fa fa-pencil-square-o" aria-hidden="true"/>
        </div>
        <div class="factor-action-text">Edit</div>
    </div>
</button>

Under Female Factor

<button class="factor-action-button p-0"
type="object"
name="action_create_repeat_consultation"
style="padding:0;">
<div class="factor-action-button">
<div class="factor-icon">
    <i title="Edit" class="fa fa-pencil-square-o" aria-hidden="true"/>
</div>
<div class="factor-action-text">Edit</div>
</div>
</button>

and wizard model is:
class EcMedicalFactorsWizard(models.TransientModel):
    _name = "ec.medical.factors.wizard"
    _description = "Wizard to select Factors"

    factor_ids = fields.Many2many('ec.medical.factors', required=1)

change action accordingly.

