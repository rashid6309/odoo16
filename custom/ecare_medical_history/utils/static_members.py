class StaticMember:

    COMPLAINS = [
        ('intermenstrual_bleeding','Intermenstrual Bleeding'),
        ('spotting', 'Spotting'),
        ('pcb', 'PCB'),
    ]

    COMPLICATIONS = [
        ('viginal_discharge','Viginal Discharge'),
        ('endometriosis', 'Endometriosis'),
        ('pid', 'PID'),
        ('fibroids', 'Fibroids'),
        ('pcos', 'PCOS'),
        ('none', 'None'),
    ]

    MONTHS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]

    SIZE_INTEGER = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
    ]

    YEARS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
    ]

    GOITEAR_LENGTH = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    GOITEAR_WIDTH = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    DAY_OF_CYCLE = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]



    MARRIAGE = [('first', '1st'),
                ('second', '2nd'),
                ('third', '3rd'),
                ('fourth', '4rth')]

    DoP = [('<6', '<6'),
           ('6', '6'),
           ('7', '7'),
           ('8', '8'),
           ('9', '9'),
           ('10', '10'),
           ('11', '11'),
           ('12', '12'), ('13', '13'),
           ('14', '14'), ('15', '15'),
           ('16', '16'), ('17', '17'),
           ('18', '18'), ('19', '19'),
           ('20', '20'), ('21', '21'),
           ('22', '22'), ('23', '23'),
           ('24', '24'),
           ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
           ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'),
           ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'),
           ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'),
           ('>40', '>40'),
           ]

    MoD = [('ABORTION', 'ABORTION'),
           ('SVD', 'SVD'),
           ('VENTOUSE', 'VENTOUSE'),
           ('FORCEPS', 'FORCEPS'),
           ('CAESAREAN', 'CAESAREAN'),
           ('MISCARRIAGE', 'MISCARRIAGE'),
           ('TOP', 'TOP'),
           ('Ectopic', 'ECTOPIC'),
           ('VBAC', 'VBAC'), ]

    GENDER = [('Male', 'Male'),
              ('Female', 'Female'),
              ('Ambiguous', 'Ambiguous'),
              ('N/A', 'N/A'), ]

    GENDER_1 = [('male', "Male"),
                ("female", "Female")]

    WEIGHT = [('<500', '<500 gms'),
              ('500', '500 gms'),
              ('600', '600 gms'),
              ('700', '700 gms'),
              ('800', '800 gms'),
              ('900', '900 gms'),
              ('1000', '1000 gms'),
              ('1100', '1100 gms'),
              ('1200', '1200 gms'),
              ('1300', '1300 gms'),
              ('1400', '1400 gms'),
              ('1500', '1500 gms'),
              ('1600', '1600 gms'),
              ('1700', '1700 gms'),
              ('1800', '1800 gms'),
              ('1900', '1900 gms'),
              ('2000', '2000 gms'),
              ('2100', '2100 gms'),
              ('2200', '2200 gms'),
              ('2300', '2300 gms'),
              ('2400', '2400 gms'),
              ('2500', '2500 gms'),
              ('2600', '2600 gms'),
              ('2700', '2700 gms'),
              ('2800', '2800 gms'),
              ('2900', '2900 gms'),
              ('3000', '3000 gms'),
              ('3100', '3100 gms'),
              ('3200', '3200 gms'),
              ('3300', '3300 gms'),
              ('3400', '3400 gms'),
              ('3500', '3500 gms'),
              ('3600', '3600 gms'),
              ('3700', '3700 gms'),
              ('3800', '3800 gms'),
              ('3900', '3900 gms'),
              ('4000', '4000 gms'),
              ('4100', '4100 gms'),
              ('4200', '4200 gms'),
              ('4300', '4300 gms'),
              ('4400', '4400 gms'),
              ('4500', '4500 gms'),
              ('4600', '4600 gms'),
              ('4700', '4700 gms'),
              ('4800', '4800 gms'),
              ('>4800', '>4800 gms'),

              ]

    HEALTH = [('N/A', 'N/A'),
              ('Alive', 'Alive'),
              ('nnd3d', 'NND in 3 days'),
              ('nnd7d', 'NND in 7 days'),
              ('nnd10d', 'NND in 10 days'),
              ('id6m', 'Infant death within 6 months'),
              ('cd6m1y', 'Child death 6 months to 1 year'),
              ('cd1y', 'Child death after 1 year'),
              ('NND-28', 'NND-28'),
              ('Died within 1 year', 'Died within 1 year'),
              ('Died within 1 month', 'Died within 1 month'),
              ]

    ALIVE = [('N/A', 'N/A'),
             ('Alive', 'Alive'),
             ('SB', 'SB'), ]

    FEED = [('Mother', 'Mother'),
            ('Artificial', 'Artificial'),
            ('N/A', 'N/A'), ]

    MENARCHE_TYPE = [
        ('regular', 'Regular'),
        ('irregular_since_menarche', 'Irregular Since Menarche'),
        ('irregular_after_regular', 'Irregular but after regular'),
        ('regular_after_irregular', 'Regular but after irregular'),
    ]

    AGE_AT_MENARCHE = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32')
    ]

    MENARCHE_CYCLE = [
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('comments', 'Comments'),
    ]
    
    MENARCHE_CYCLE_DAYS = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    ]
        
    MENARCHE_CYCLE_MONTHS = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6')
    ]

    MENSTRUAL_FLOW = [
        ('normal', 'Normal'),
        ('scanty', 'Scanty'),
        ('excessive', 'Excessive'),
    ]

    DYSMENORRHOEA = [
        ('before_menses', 'Before Menses'),
        ('during_menses', 'During Menses'),
        ('after_menses', 'After Menses'),
        ('none', 'None'),
    ]

    INTENSITY = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
        ('none', 'None'),
    ]

    SIDE = [
        ('right', "Right"),
        ('left', "Left"),
    ]

    SIZE = [
        ('normal', "Normal"),
        ('small', "Small"),
        ('large', "Large")
    ]

    FAMILY_LIVING_STYLE = [('joint', 'Joint'),
                           ('independent', 'Independent')]

    MARRIAGE_RELATION = [('first_cousin', '1st Cousin'),
                         ('second_cousin', '2nd Cousin'),
                         ('distant_relatives', 'Distant Relatives'),
                         ('not_related', 'Not Related')]

    CHOICE_YES_NO = [('yes', "Yes"),
                     ('no', "No")]

    ORGAN_SIZE = [('normal', 'Normal'),
                  ('other', 'Other'),
                  ]

    UTERUS_SIZE = [('healthy', 'Healthy'),
                   ('other', 'Other'),
                   ]

    UTERUS_MOBILITY = [('mobile', 'Mobile'),
                       ('Restricted', 'Restricted'),
                       ]

    UTERUS_POSITION = [('a/v', 'A/V'),
                       ('r/v', 'R/V'),
                       ('mid_position', 'Mid-Position'),
                       ]

    UTERUS_SIZE_POSITION = [
        ('deviated_to_right', 'Deviated To Right'),
        ('deviated_to_left', 'Deviated To Left'),
        ('a/v', 'A/V'),
        ('r/v', 'R/V'),
        ('m/p', 'M/P'),
    ]

    THYROID = [('palpable', 'Palpable'),
               ('non_palpable', 'Non Palpable'),
               ]

    THYROID_GOITEAR_TYPE = [('mobile', 'Mobile'),
                            ('fixed', 'Fixed'),
                            ]

    PALLOR = [('present', 'Present'),
              ('absent', 'Absent'),
              ]

    OVARY_SIZE = [('active', 'Active'),
                  ('quite', 'Quite'),
                  ('cyst', 'Cyst'),
                  ('pcos', 'PCOs'),
                  ('not_visualized', 'Not Visualized'),
                  ]

    UTERUS_TYPE_SIZE = [('size', 'Size'),
                        ('position', 'Position'),
                        ('cyst', 'Cyst'),
                        ('pcos', 'PCOs'),
                        ('not_visualized', 'Not Visualized'),
                        ]

    UTERUS_NOS = [('size', 'Size'),
                  ('position', 'Position'),
                  ('cyst', 'Cyst'),
                  ('pcos', 'PCOs'),
                  ('not_visualized', 'Not Visualized'),
                  ]

    UTERUS_TVS = [
        ('size', 'Size'),
        ('position', 'Position'),
        ('normal', 'Normal'),
        ('fibroid', 'Fibroid'),
    ]

    FORBID = [('smooth', 'Smooth'),
              ('distorted', 'Distorted'),
              ('triple_echo', 'Triple Echo'),
              ]

    LINING = [('smooth', 'Smooth'),
              ('distorted', 'Distorted'),
              ('triple_echo', 'Triple Echo'),
              ]

    LINING_SIZE = [('smooth', 'Smooth'),
                   ('distorted', 'Distorted'),
                   ('triple_echo', 'Triple Echo'),
                   ]

    SX_ISSUES = [
        ('aparunea', 'Aparunea'),
        ('dysparunea', 'Dysparunea'),
        ('none', 'None'),
    ]

    CN_TYPES = [
        ('none', 'None'),
        ('withdrawal', 'Withdrawal'),
        ('condom', 'Condom'),
        ('foam', 'Foam'),
        ('ocp', 'OCP'),
        ('injectable', 'Injectable'),
        ('iucd', 'IUCD'),
    ]

    SX_PERFORMANCE = [
        ('adequate', 'Adequate'),
        ('inadequate', 'Inadequate'),
    ]

    MEDICAL_THYROID = [
        ('Hypothyroidism', 'Hypothyroidism'),
        ('Hyperthyroidism', 'Hyperthyroidism')
    ]

    DIABETES_TYPE = [
        ('IDDM', 'IDDM or type 1'),
        ('NIDDM', 'NIDDM or type 2')
    ]

    INFERTILITY = [
        ('primary_infertility', 'Primary Infertility'),
        ('secondary_infertility', 'Secondary Infertility')
    ]

    PREVIOUS_TREATMENT_TYPE = [
        ('ovulation_induction_intercourse', 'Ovulation Induction / Timed Sexual Intercouse'),
        ('intra_uterine', 'Intra - Uterine Insemination'),
        ('in_vitro_fertilization', 'In - Vitro Fertilization'),
    ]

    ULTRASOUND_TYPE = [
        ('abdominal', "Abdominal"),
        ("tvs", "TVS"),
        ("both", "Both"),
    ]

    LABOUR_HISTORY = [
        ('spontaneous', 'Spontaneous'),
        ('induced', 'Induced'),
    ]

    LOCATION = [
        ('sudi_pak', 'Sudi Pak'),
        ('jannah_super', 'Jannah Super'),
    ]

    REPEAT_STATUS = [
        ('walkin', 'Walk-in Visit'),
        ('appointment', 'Appointment'),
    ]

    REPEAT_CONSULTATION_TYPE = [
        ('in_person', 'In-person Consultation'),
        ('telephonic', 'Telephonic Consultation'),
        ('online', 'Online Consultation'),
    ]

    SEEN_WITH = [
        ('couple', "Couple"),
        ('wife', "Wife"),
        ('husband', "Husband"),
        ('others', "Others")
    ]

    MULTI_SELECTION_FIELD = [
        ('lining', 'Lining'),
        ('complications', 'Complications'),
        ('complains', 'Complains'),
        ('dysmenorrhoea', 'Dysmenorrhoea'),
        ('position', 'Position'),
    ]
    
    CHOICE_YES_NO_NA = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('na', 'NA'),
    ]

    PELVIC_EXAM_CHOICES = [
        ('inspection', 'Inspection only'),
        ('p/v', 'P/V'),
        ('p/s', 'P/S'),
    ]

    METHOD_OF_HVS = [
        ('self_swab', 'Self swab without speculum'),
        ('operator_swab', 'Operator swab without speculum'),
        ('speculum_swab', 'Speculum swab'),
    ]

    CYST_TYPE = [
        ('solid', 'Solid'),
        ('provide1', 'Provide'),
        ('provide2', 'Provide'),
    ]

    OVARY_TYPE = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]
