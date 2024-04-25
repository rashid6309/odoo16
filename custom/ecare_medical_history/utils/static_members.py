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

    UTERUS_FLEXION = [
        ('A/V', 'A/V'),
        ('R/V', 'R/V'),
        ('unable_to_determine', 'Unable to Determine'),
    ]

    YEARS = [
        ('<1', 'Less than 1'),
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
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'),
        ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'),
        ('59', '59'), ('60', '60')
    ]

    MONTHS_MEDICAL = [
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
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36')
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
                ('fourth', '4th'),
                ('unmarried', 'Unmarried')
                ]

    SIGN_OVULATION = [('free_fluid', 'Free Fluid'),
                      ('loss_of_dominant_follicle', 'Loss of Dominant Follicle(s)'),
                      ('irregular_follicle', 'Irregular Follicle(s)'),
                      ('corpus_luteum', 'Corpus Luteum'),
                      ]

    TVS_DIAGNOSIS = [
        ('early_mid_follicular', 'Early-Mid Follicular Phase'),
        ('late_follicular', 'Late Follicular Phase'),
        ('pre_ovulation', 'Pre-Ovulation'),
        ('recent_ovulation', 'Recent Ovulation'),
        ('late_luteal_pre_menstrual', 'Late Luteal Phase/Pre-Menstrual'),
        ('luf', 'LUF'),
        ('post_menopausal', 'Post-Menopausal'),
        ('pre_menarche', 'Pre-Menarche'),
        ('uncertain', 'Uncertain'),
    ]

    TYPE_CONCEPTION = [('natural', 'Natural'),
                       ('assisted', 'Assisted'),
                       ]

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
           ('VBAC', 'VBAC'),
           ('r_tubal', 'R TUBAL ECTOPIC'),
           ('l_tubal', 'L TUBAL ECTOPIC'),
           ('tubal_ectopic', 'TUBAL ECTOPIC SIDE UNKNOWN'),
           ('ectopic_other', 'ECTOPIC OTHER'),
           ]

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
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
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

    MENSTRUAL_CYCLE_TO = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
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
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52'),
        ('53', '53'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('59', '59'),
        ('60', '60'),
        ('61', '61'),
        ('62', '62'),
        ('63', '63'),
        ('64', '64'),
        ('65', '65'),
        ('66', '66'),
        ('67', '67'),
        ('68', '68'),
        ('69', '69'),
        ('70', '70'),
        ('71', '71'),
        ('72', '72'),
        ('73', '73'),
        ('74', '74'),
        ('75', '75'),
        ('76', '76'),
        ('77', '77'),
        ('78', '78'),
        ('79', '79'),
        ('80', '80'),
        ('81', '81'),
        ('82', '82'),
        ('83', '83'),
        ('84', '84'),
        ('85', '85'),
        ('86', '86'),
        ('87', '87'),
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
        ('93', '93'),
        ('94', '94'),
        ('95', '95'),
        ('96', '96'),
        ('97', '97'),
        ('98', '98'),
        ('99', '99'),
        ('100', '100'),
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

    CHOICE_YES_NO_NOT_AVAILABLE = [('yes', "Yes"),
                                   ('no', "No"),
                                   ('not_available', "Not Available")
                                   ]

    ORGAN_SIZE = [('normal', 'Normal'),
                  ('other', 'Other'),
                  ]

    UTERUS_SIZE = [('healthy', 'Healthy'),
                   ('other', 'Other'),
                   ]

    UTERUS_MOTILITY = [('mobile', 'Mobile'),
                       ('restricted', 'Restricted'),
                       ]

    UTERUS_POSITION = [
        ('mid_position', 'Mid Position'),
        ('deviated_to_right', 'Deviated to RIGHT'),
        ('deviated_to_left', 'Deviated to LEFT'),
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

    OVARY_SIZE_TYPE = [('hypo', 'Hypo'),
                       ('hyper', 'Hyper'),
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

    PREVIOUS_TREATMENT_OUTCOME = [
        ('pregnancy', 'Pregnancy'),
        ('no_pregnancy', 'No Pregnancy'),
        ('ABORTION', 'ABORTION'),
        ('SVD', 'SVD'),
        ('VENTOUSE', 'VENTOUSE'),
        ('FORCEPS', 'FORCEPS'),
        ('CAESAREAN', 'CAESAREAN'),
        ('MISCARRIAGE', 'MISCARRIAGE'),
        ('TOP', 'TOP'),
        ('Ectopic_Right', 'ECTOPIC RIGHT'),
        ('Ectopic_Left', 'ECTOPIC LEFT'),
        ('VBAC', 'VBAC'),
        ('NA', 'N/A'),
    ]

    PREVIOUS_TREATMENT_OF = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('couple', 'Couple'),
    ]

    PREVIOUS_TREATMENT_RESPONSE = [
        ('poor', 'Poor'),
        ('good', 'Good'),
        ('ver_good', 'Very Good'),
    ]

    ULTRASOUND_TYPE = [
        ('abdominal', "Abdominal"),
        ("tvs", "TVS"),
        ("both", "Both"),
    ]

    LABOUR_HISTORY = [
        ('spontaneous', 'Spontaneous'),
        ('induced', 'Induced'),
        ('na', 'N/A'),
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
        ('migration', 'Migration'),
    ]

    SEEN_WITH = [
        ('couple', "Couple"),
        ('wife', "Wife"),
        ('husband', "Husband"),
        ('others', "Others")
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
        ('unable_determine', 'Unable to Determine'),
    ]

    SEMEN_COLOR = [
        ('creamy_white', 'Creamy White'),
        ('yellow', 'Yellow'),
        ('pale', 'Pale'),
        ('straw', 'Straw'),
    ]

    SEMEN_VISCOSITY = [
        ('thick', 'Thick'),
        ('thin', 'Thin'),
        ('viscous', 'Viscous'),
        ('normal', 'Normal'),
    ]

    SEMEN_MOTILITY = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
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
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52'),
        ('53', '53'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('59', '59'),
        ('60', '60'),
        ('61', '61'),
        ('62', '62'),
        ('63', '63'),
        ('64', '64'),
        ('65', '65'),
        ('66', '66'),
        ('67', '67'),
        ('68', '68'),
        ('69', '69'),
        ('70', '70'),
        ('71', '71'),
        ('72', '72'),
        ('73', '73'),
        ('74', '74'),
        ('75', '75'),
        ('76', '76'),
        ('77', '77'),
        ('78', '78'),
        ('79', '79'),
        ('80', '80'),
        ('81', '81'),
        ('82', '82'),
        ('83', '83'),
        ('84', '84'),
        ('85', '85'),
        ('86', '86'),
        ('87', '87'),
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
        ('93', '93'),
        ('94', '94'),
        ('95', '95'),
        ('96', '96'),
        ('97', '97'),
        ('98', '98'),
        ('99', '99'),
        ('100', '100'),
    ]

    SEMEN_SIGN_VALUES = [
        ('nil', 'Nil'),
        ('+', '+'),
        ('++', '++'),
        ('+++', '+++'),
    ]

    SEMEN_MORPHOLOGY = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
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
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52'),
        ('53', '53'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('59', '59'),
        ('60', '60'),
        ('61', '61'),
        ('62', '62'),
        ('63', '63'),
        ('64', '64'),
        ('65', '65'),
        ('66', '66'),
        ('67', '67'),
        ('68', '68'),
        ('69', '69'),
        ('70', '70'),
        ('71', '71'),
        ('72', '72'),
        ('73', '73'),
        ('74', '74'),
        ('75', '75'),
        ('76', '76'),
        ('77', '77'),
        ('78', '78'),
        ('79', '79'),
        ('80', '80'),
        ('81', '81'),
        ('82', '82'),
        ('83', '83'),
        ('84', '84'),
        ('85', '85'),
        ('86', '86'),
        ('87', '87'),
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
        ('93', '93'),
        ('94', '94'),
        ('95', '95'),
        ('96', '96'),
        ('97', '97'),
        ('98', '98'),
        ('99', '99'),
        ('100', '100'),
    ]

    SEMEN_METHOD = [
        ('none', 'None'),
        ('swim_up', 'Swim Up'),
        ('single_gradient', 'Single Gradient'),
        ('double_gradient', 'Double Gradient')
    ]
    CONCEPTION_TYPE = [('natural', 'Natural'),
                       ("oi", "OI"),
                       ("natural iui", "Natural IUI"),
                       ("oi/ui", "OI/UI"),
                       ("fresh et", "Fresh ET"),
                       ("fer", "FER")]

    GESTATION_TYPE = [('singleton', 'Singleton'),
                      ('dcda_twins', 'DCDA Twins'),
                      ('mcda_twins', 'MCDA Twins'),
                      ('momo_twins', 'MoMo Twins'),
                      ('triplets', 'Triplets'),
                      ('quadruplets', 'Quadruplets'),
                      ('pentaplets', 'Pentaplets (5)'),
                      ('sextuplets', 'Sextuplets (6)'),
                      ('septuplets', 'Septuplets (7)'),
                      ('octuplets', 'Octuplets (8)'),
                      ("other", "Other")]

    VIABILITY_POTENTIAL = [("all_fetus_alive", "All fetus(es) alive"),
                           ("iud", "IUD"),
                           ("atleat_1_alive", "Atleast 1 alive fetus"),
                           ("missed_miscarriage", "Missed miscarriage"),
                           ("incomplete_miscarriage", "Incomplete miscarriage"),
                           ("complete_miscarriage", "Complete miscarriage"),
                           ("theatened_miscarriage", "Theatened miscarriage"),
                           ("inevitable_miscarriage", "Inevitable miscarriage"),
                           ("ectopic", "Ectopic"),
                           ]

    VISIT_REASON = [('early_pregnancy_assessment', 'Early pregnancy management'),
                    ('genetic_testing', 'Genetic Testing')]

    FETAL_HEART = [("positive", "Positive"),
                   ("negative", "Negative")]

    RHYTHM_TYPE = [('regular', 'Regular'),
                   ('irregular', 'Irregular')]

    AGE_WEEKS = [
        ('1', '01 week'),
        ('2', '02 weeks'),
        ('3', '03 weeks'),
        ('4', '04 weeks'),
        ('5', '05 weeks'),
        ('6', '06 weeks'),
        ('7', '07 weeks'),
        ('8', '08 weeks'),
        ('9', '09 weeks'),
        ('10', '10 weeks'),
        ('11', '11 weeks'),
        ('12', '12 weeks'),
        ('13', '13 weeks'),
        ('14', '14 weeks'),
        ('15', '15 weeks'),
        ('16', '16 weeks'),
        ('17', '17 weeks'),
        ('18', '18 weeks'),
        ('19', '19 weeks'),
        ('20', '20 weeks'),
        ('21', '21 weeks'),
        ('22', '22 weeks'),
        ('23', '23 weeks'),
        ('24', '24 weeks'),
        ('25', '25 weeks'),
        ('26', '26 weeks'),
        ('27', '27 weeks'),
        ('28', '28 weeks'),
        ('29', '29 weeks'),
        ('30', '30 weeks'),
        ('31', '31 weeks'),
        ('32', '32 weeks'),
        ('33', '33 weeks'),
        ('34', '34 weeks'),
        ('35', '35 weeks'),
        ('36', '36 weeks'),
        ('37', '37 weeks'),
        ('38', '38 weeks'),
        ('39', '39 weeks'),
        ('40', '40 weeks'),
        ('>40', '>40 weeks'),
    ]

    UPT_RESULT = [
        ('negative', 'Negative'),
        ('not_done', 'Not Done'),
        ('positive', 'Positive'),
    ]

    PRIMARY_INDICATION = [
        ('no_plan', 'No current plan'),
        ('erectile_dysfunction', 'Erectile dysfunction'),
        ('premature_ejaculation', 'Premature ejaculation'),
        ('female_sexual_dysfunction', 'Female sexual dysfunction'),
        ('vaginismus', 'Vaginismus'),
        ('cervical_hostility', 'Suspicion of cervical hostility'),
        ('couple_request', 'Couple request'),
        ('previous_iui', 'Previous successful IUI'),
        ('husband_not_present', 'Husband not present'),
    ]

    IUI_DROPDOWN = [
        ('not_tested', 'Not tested'),
        ('both_patent', 'Both patent'),
        ('r_only', 'R only (free spill)'),
        ('l_only', 'L only (free spill)'),
        ('both_blocked', 'Both blocked'),
        ('restricted_spill', 'Restricted Spill'),
    ]

    UTERINE_TUBAL_ANOMALIES = [
        ('hsg', 'HSG'),
        ('hycosy', 'HyCoSy'),
        ('icsi_scan', 'ICSI Scan'),
        ('radiology_scan', 'Radiology Scan'),
        ('no_testing', 'No testing done for uterine anomalies'),
    ]

    FSH_LH_AMH_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('awaiting_results', 'Updated results await'),
    ]

    TRIGGER_REGIMEN = [
        ('ivf_c_10', 'IVF-C 10,000IU S/C'),
        ('ovidrel_250_mcg', 'Ovidrel 250mcg S/C'),
    ]

    SCHEDULE = [
        ('appointment', 'Appointment'),
        ('documented_ultrasound', 'Documented Ultrasound'),
        ('blood_tests', 'Blood Tests'),
    ]

    INTERVENTION = [
        ('trigger_inseminate', 'Ready to trigger & inseminate'),
        ('2nd_trigger', '2nd trigger'),
        ('luteal_phase_support', 'Luteal phase support'),
    ]

    INSEMINATION = [
        ('natural', 'Natural'),
        ('fresh_iui', 'Fresh IUI'),
        ('frozen_thawed_iui', 'Frozen-thawed IUI'),
    ]

    INDICATION_OF_IUI = [
        ('erectile_dysfunction', 'Erectile dysfunction'),
        ('converted_natural', 'Converted from natural'),
        ('premature_ejaculation', 'Premature ejaculation'),
        ('female_sexual_dysfunction', 'Female sexual dysfunction'),
        ('vaginismus', 'Vaginismus'),
        ('cervical_hostility', 'Suspicion of cervical hostility'),
        ('couple_request', 'Couple request'),
        ('previous_iui', 'Previous successful IUI'),
        ('husband_not_present', 'Husband not present'),
    ]

    LUTEAL_PHASE_SUPPORT = [
        ('c', 'C'),
        ('c_d_2', 'C + D2'),
        ('c_d_3', 'C + D3'),
    ]

    PREPARATION_METHOD = [
        ('iui_only', 'IUI only, no ovulation induction agents'),
        ('ol_clomiphene_50mg', 'Ol with clomiphene citrate, 50mg OD, from cycle days 2 to 5'),
        ('ol_clomiphene_100mg', 'Ol with clomiphene citrate, 100mg OD, from cycle days 2 to 5'),
        ('ol_clomiphene_150mg', 'Ol with clomiphene citrate, 150mg OD, from cycle days 2 to 5'),
        ('ol_clomiphene_200mg', 'Ol with clomiphene citrate, 200mg OD, from cycle days 2 to 5'),
        ('ol_clomiphene_250mg', 'Ol with clomiphene citrate, 250mg OD, from cycle days 2 to 5'),
        ('ol_letrozole_2.5mg', 'Ol with Letrozole, 2.5mg OD, from cycle days 2 to 5'),
        ('ol_letrozole_5mg', 'Ol with Letrozole, 5mg OD, from cycle days 2 to 5'),
    ]

    SIGN_OF_OVULATION = [
        ('free_fluid', 'Free fluid'),
        ('loss_of_dominant_follicles', 'Loss of dominant follicle(s)'),
        ('irregular_follicles', 'Irregular follicle(s)'),
        ('corpus_luteum', 'Corpus luteum'),
    ]

    OI_TI_ATTEMPT_STATE = [
        ('in_progress', 'Attempt in progress'),
        ('completed', 'Attempt Completed'),
        ('abandoned', 'Attempt Abandoned'),
    ]

    OI_TI_PLATFORM_STATE = [
        ('ready_to_trigger', 'Ready to trigger & inseminate'),
        ('2nd_trigger', '2nd trigger'),
        ('luteal_phase', 'Luteal phase support'),
    ]

    SURGERY_TYPES = [
        ('tubal_patency_testing', 'Tubal Patency Testing'),
        ('minimally_invasive_surgery', 'Minimally Invasive Surgery Other Than Tubal Testing'),
        ('laparotomy', 'Laparotomy'),
        ('cardiac_surgery', 'Cardiac Surgery'),
        ('neurosurgery', 'Neurosurgery'),
        ('surgery_for_cancer', 'Surgery for Cancer'),
        ('other', 'Other'),
    ]

    SURGERY_TYPES_MALE = [
        ('minimally_invasive_surgery', 'Minimally Invasive Surgery'),
        ('laparotomy', 'Laparotomy'),
        ('cardiac_surgery', 'Cardiac Surgery'),
        ('neurosurgery', 'Neurosurgery'),
        ('surgery_for_cancer', 'Surgery for Cancer'),
        ('other', 'Other'),
    ]

