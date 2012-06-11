#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORD_CLASSES = {'N':'Nouns', 
                'PROP':'Proper nouns', 
                'SPEC': 'Specifiers', 
                'DET': 'Determiners',
                'PERS':'Personal pronouns', 
                'ADJ':'Adjectives',
                'ADV':'Adverbs', 
                'V':'Verbs', 
                'NUM':'Numerals', 
                'PRP':'Preposition',
                'KS':'Subordinating conjunctions',
                'KC':'Coordinationg conjunctions',
                'IN':'Interjections',
                'EC':'Hyphen-separated prefix',}

INF_TAGS = {'M':'Male gender', 
            'F':'Female gender', 
            'M/F':'Neutral gender',
            'S':'Singular number', 
            'P':'Plural number', 
            'S/P':'Neutral number',
            'NOM':'Nominative case', 
            'ACC':'Accusative case', 
            'DAT':'Dative case',
            'PIV':'Prepositive case', 
            'ACC/DAT':'Accusative-Dative case', 
            'DAT':'Nominative-Prepositive case', 
            '1':'First person', 
            '2':'Second person', 
            '3':'Third person',
            '1S':'First person singular', 
            '2S':'Second person singular',
            '3S':'Third person singular',
            '1P':'First person plural', 
            '2P':'Second person plural',
            '3P':'Third person plural',
            '1/3S':'First or Third person singular', 
            '0/1/3S':'Impersonal or First or Third person singular',
            'PR':'presente simples',
            'IMPF':'preterito imperfeito', 
            'PS':'preterito perfeito',
            'MQP':'preterito mais-que-perfeito', 
            'FUT':'futuro do presente', 
            'COND':'futuro do preterito',
            'IND':'indicativo', 
            'SUBJ':'subjuntivo', 
            'IMP':'imperativo', 
            'VFIN':'Verbo Finito',
            'INF':'infinitivo', 
            'PCP':'participio', 
            'GER':'gerundio'}

SYN_TAGS = {'@SUBJ>':'subject', 
            '@<SUBJ':'subject',
            '@ACC>':'accusative direct object',
            '@<ACC':'accusative direct object', 
            '@DAT>':'dative object only pronominal', 
            '@<DAT':'dative object only pronominal',
            '@PIV>':'prepositional indirect object', 
            '@<PIV':'prepositional indirect object',
            '@ADVS> / @SA>':'adverbial object (place, time, duration, quantity), subject-related',
            '@<ADVS / @<SA':'adverbial object (place, time, duration, quantity), subject-related',
            '@ADVO> / @OA>':'adverbial object object-related',
            '@<ADVO / @<OA':'adverbial object object-related',
            '@SC>':'subject predicative',
            '@<SC':'subject predicative',
            '@OC>':'object predicative',
            '@<OC':'object predicative',
            '@ADVL>':'adverbial',
            '@<ADVL':'adverbial',
            '@PASS>':'agent of passive',
            '@<PASS':'agent of passive', #All above clause arguments attach to the nearest main verb to the left [<] or right [>]
            '@ADVL':'free adverbial phrase in non-sentence expression',
            '@NPHR':'free noun phrase in non-sentence expression without verbs',
            '@VOK':'vocative',
            '@>N':'prenominal adject', 
            '@N<':'postnominal adject', #both last attaches to the nearest NP-head that is not an adnominal itself
            '@N<PRED':'postnominal in-group predicative', #or predicate in small clause introduced by com/sem',
            '@APP':'identifying apposition',
            '@>A':'prepositioned adverbial adject', #attaches to the nearest ADJ/PCP/ADV or attributive used N to the right 
            '@A<': 'postpositioned adverbial adject', #or dependent/argument of attributive participle (with function tag attached
            '@PRED>': 'forward free predicative', #refers to the following @SUBJ, even when this is incorporated in the VP 
            '@<PRED': 'backward free predicative', #refers to the nearest NP-head to the left, or to the nearest @SUBJ to the left
            '@P<': 'argument of preposition', 
            '@S<': 'sentence anaphor', 
            '@FAUX': 'finite auxiliary',
            '@FMV': 'finite main verb', 
            '@IAUX': 'infinite auxiliary', 
            '@IMV': 'infinite main verb', 
            '@PRT-AUX<': 'verb chain particle',
            '@CO': 'coordinating conjunction', 
            '@SUB': 'subordinating conjunction', 
            '@KOMP<': 'argument of comparative',
            '@COM': 'direct comparator without preceding comparative',
            '@PRD': 'role predicator',
            '@FOC>': 'focus marker',
            '@<FOC': 'focus marker',
            '@TOP': 'topic constituent',
            '@#FS-': 'finite subclause', #combines with clausal role and intraclausal word tag, e.g.@#FS-<ACC @SUB for "não acredito que seja verdade") 
            '@#ICL-': 'infinite subclause', #combines with clausal role and intraclausal word tag, e.g. @#ICL-SUBJ> @IMV in "consertar um relógio não é fácil") 
            '@#ICL-AUX<': 'argument verb in verb chain', #refers to preceding auxiliary (the verb chain sequence @FAUX - @#ICL-AUX< is used, where both verbs have the same subject, @FMV - @#ICL-<ACC is used where the subjects are different) 
            '@#AS-': 'averbal subclause', #combines with clausal role and intraclausal word tag, e.g. @#AS-<ADVL @ADVL> in "ajudou onde possível") 
            '@AS<': 'argument of complementiser in averbal subclause'}

SUB_TAGS = {'<artd>': 'definite article', # (DET)
            '<arti>': 'indefinite article', # (DET)
            '<quant>': 'quantifier pronoun', #(DET: <quant1>, <quant2>, <quant3>, SPEC: <quant0>) or intensifier adverb 
            '<dem>': 'demonstrative pronoun', #(DET: <dem> SPEC: <dem0>) 
            '<poss>': 'possessive pronoun', # (DET) 
            '<refl>': 'reflexive personal pronoun', # ("se" PERS ACC, "si" PERS PIV) 
            '<si>': 'reflexive use of 3. person possessive', 
            '<reci>': 'reciprocal use of reflexive pronoun', #(= "um ao outro") 
            '<coll>': 'collective reflexive', # ("reunir-se", "associar-se") 
            '<diff>': 'differentiator', #(DET) (e.g. "e outros temas", "a mesma diferença") 
            '<ident>': 'identator', #(DET) (e.g. "o próprio usuário", "a si mesmo") 
            '<rel>': 'relative pronoun', #(DET, SPEC) 
            '<interr>': 'interrogative pronoun', #(DET, SPEC) 
            '<post-det>': 'typically located as post-determiner', #(DET @N'<) 
            '<post-attr>': 'typically post-positioned adjective', #(ADJ @N'<) 
            '<ante-attr>': 'typically pre-positioned adjective', #  (ADJ @>': 'N) 
            '<adv>': 'can be used adverbially', # (ADJ @ADVL) 
            '<ks>': 'relative adverb used like a subordinating conjunction',
            '<kc>': 'conjunctional adverb', # (pois, entretanto)
            '<det>': 'determiner usage/inflection of adverb', #("ela estava toda nua.") 
            '<foc>': 'focus marker adverb', # (also forms of "ser") 
            '<prp>': 'relative adverb used like a preposition', 
            '<KOMP>': '<igual>', # equalling" comparative (ADJ, ADV) (e.g. "tanto", "tão") 
            '<KOMP>': '<corr>', # correlating comparative (ADJ, ADV) (e.g. "mais velho", "melhor") 
            '<komp>': '<igual>', # equalling" particle referring to comparative (e.g. "como", "quanto") 
            '<komp>': '<corr>', # correlating" particle referring to comparative (e.g. "do=que") 
            '<SUP>': 'superlative', 
            '<setop>': 'operational adverb', # (eg. "não", "nunca", "ja'", "mais" in "não mais") 
            '<dei>': 'discourse deictics', # (e.g. "aqui", "ontem") 
            '<card >': 'cardinal', # (NUM) 
            '<NUM-ord>': 'ordinal', #(ADJ) 
            '<NUM-fract>': 'fraction-numeral', # (N) 
            '<cif>': 'cipher', #<card>'NUM, <NUM-ord>, ADJ
            '<sam->': 'first part of morphologically fused word pair', #("de" in "dele") 
            '<-sam>': 'last part of morphologically fused word pair', #("ele" in "dele") 
            '<*>': '1. letter capitalized', 
            '<*1>': 'left quote attached', 
            '<*2>': 'right quote attached', 
            '<hyfen>': 'hyphenated word', 
            '<ABBR>': 'abbreviation', 
            '<prop>': 'noun, adjective etc. used as name' , #(upper case initial in mid-sentence) 
            '<n>': 'adjective or participle used as a noun', # typically as head of a nominal phrase 
            '<fmc>': 'finite main clause heading verb ',
            '<co-acc>': '',
            '<co-advl>': '',
            '<co-app>': '',
            '<co-dat>': '',
            '<co-fmc>': '',
            '<co-ger>': '',
            '<co-inf>': '',
            '<co-oc>': '',
            '<co-pcv>': '',
            '<co-postad>': '',
            '<co-postnom>': '',
            '<co-pred>': '',
            '<co-prenom>': '',
            '<co-prparg>': '',
            '<co-sc>': '',
            '<co-subj>': '',
            '<co-vfin>': ''} #co-ordinator tags indicating what is co-ordinated


VALENCY_TAGS = {'<vt>': 'monotransitive verb with accusative object', 
                '<vi>': '<ve> intransitive verb (ergative verb)', 
                '<vtd>': 'ditransitive verb with accusative and dative objects',
                '<PRP^vp>': 'monotransitive verb with prepositional object', # (headed by PRP) 
                '<PRP^vtp>': 'ditransitive verb with accusative and prepositional objects', 
                '<vK>': 'copula verb with subject predicative', 
                '<vtK>': 'copula verb with object predicative', 
                '<va>': 'transitive verb with adverbial argument', 
                '<va+LOC>': '',
                '<va+DIR>': '',
                '<vta+LOC>': '',
                '<vta+DIR>': '',
                '<vt+QUANT>': 'transitive verb with NP as quantitative adverbial object', #(e.g. "pesar")
                '<vt+TID>': ' transitive verb with NP as temporal adverbial object', #(e.g. "durar") 
                '<vU>': 'impersonal verbs (normally in the 3S-person', #e.g. "chove") 
                '<x>': 'auxiliary verb with infinitive', #(tagged @(F)AUX - @#ICL-AUX'<) 
                '<x+PCP>': 'auxiliary verb with participle', #(tagged @(F)AUX - @#ICL-AUX'<) 
                '<x+GER>': 'auxiliary verb with gerund', #(tagged @(F)AUX - @#ICL-AUX'<) 
                '<PRP^xp>': 'auxiliary verb with (prepositional) auxiliary particle and infinitive', #(tagged as @(F)AUX - @PRT-AUX'< - @#ICL-AUX'<) 
                '<xt>': 'auxiliary verb with infinitive clause subject in the accusative case', # and ACI-constructions', #(both tagged as @(F)MV - @SUBJ>': ' - @#ICL-ACC) 
                '<PRP^xtp>': 'auxiliary verb with accusative object and prepositional object containing an infinitive clause with its (unexpressed) subject being identical to the preceding accusative object', # (tagged as @(F)MV - @'<ACC - @'<PIV - @#ICL-P'<) 
                '<vr>': 'reflexive verbs', # (also '<vrp>': ', '<vaux-r>': ', '<vaux-rp>': ') 
                '<vq>': 'cognitive" verb governing a que-sentence', 
                '<qv>': 'impersonal" verb with que-subclause as subject predicative', #("parece que", "consta que") 
                '<+interr>': 'discourse" verb or nominal governing an interrogative subclause', 
                '<+n>': 'noun governing a name', # (PROP) (e.g. "o senhor X") 
                '<+num>': 'noun governing a number', #(e.g. "cap. 7", "no dia 5 de dezembro") 
                '<num+>': 'unit" noun', # (e.g. "20 metros") 
                '<+INF>': 'governs infinitive', # (N, ADJ) 
                '<+PRP>': 'governs prepositional phrase headed by PRP', #e.g. '<+sobre>': ' 
                '<PRP+>': 'typically argument of preposition PRP',
                '<+que>': '',
                '<+PRP+que>': 'nominal governing a que-subclause'} #(N, ADJ)