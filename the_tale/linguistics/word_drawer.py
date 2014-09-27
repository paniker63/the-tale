# coding: utf-8
import jinja2

from utg import words
from utg import data as utg_data
from utg import relations as utg_relations

from the_tale.linguistics import relations


def get_best_base(word_type):
    best_base = None
    best_size = -1

    for base in relations.WORD_BLOCK_BASE.records:
        if set(base.schema).issubset(set(word_type.schema)) and len(base.schema) > best_size:
            best_size = len(base.schema)
            best_base = base

    return best_base


def get_structure(word_type):

    schema = word_type.schema

    base = get_best_base(word_type=word_type)

    iterated = [property for property in schema if property not in base.schema]

    data = []

    iterated_keys = set()

    for key in utg_data.INVERTED_WORDS_CACHES[word_type]:
        iterated_keys.add(tuple(k for k, p in zip(key, word_type.schema) if p in iterated))

    iterated_keys = sorted(iterated_keys,
                           key=lambda x: tuple(r.value if r is not None else -1 for r in x))

    for key in iterated_keys:
        data.append(Leaf(type=word_type,
                         base=base,
                         key={p:k for p, k in zip(iterated, key)}))

    return data


class Leaf(object):

    def __init__(self, type, base, key):
        self.type = type
        self.key = key
        self.base = self.choose_base(base)

    def get_header_properties(self):
        keys = [self.key[property] for property in self.type.schema if self.key.get(property) is not None]
        keys.sort(key=lambda r: self.type.schema.index(r._relation))
        return keys

    def get_form_key(self, base_key):
        key = {base_properties: base_properties.records[base_key[i]] if base_key[i] is not None else None
               for i, base_properties in enumerate(self.base.schema)}
        key.update(self.key)
        key = tuple(key.get(relation) for relation in self.type.schema)
        return key

    def choose_base(self, base):
        real_properties = tuple(property
                                for property in base.schema
                                if all(property not in utg_data.RESTRICTIONS.get(key, []) for key in self.key.values() if key is not None))
        return relations.WORD_BLOCK_BASE.index_schema[real_properties]


class BaseDrawer(object):

    def __init__(self, type):
        self.type = type

    def get_header(self, properties):
        return u', '.join([k.text for k in properties])

    def get_form(self, key):
        raise NotImplementedError()

    def get_property(self, property):
        raise NotImplementedError()


class FormDrawer(BaseDrawer):

    def __init__(self, type, form):
        super(FormDrawer, self).__init__(type=type)
        self.form = form

    def get_form(self, key):
        cache = utg_data.WORDS_CACHES[self.type]

        if key not in cache:
            return u''

        return self.form['field_%d' % cache[key]].widget

    def get_property(self, property):
        return self.form['field_%s' % property.__name__].widget


class ShowDrawer(BaseDrawer):

    def __init__(self, word):
        super(ShowDrawer, self).__init__(type=word.type)
        self.word = word

        word_parent = self.word.get_parent()

        self.other_version = word_parent if word_parent else self.word.get_child()

    def get_form(self, key):
        cache = utg_data.WORDS_CACHES[self.type]

        if key not in cache:
            return u''

        form = self.word.utg_word.form(words.Properties(*key))
        other_form = self.other_version.utg_word.form(words.Properties(*key)) if self.other_version else None

        if other_form is None or form == other_form:
            html = form
        else:
            html = u'<span class="changed-word" rel="tooltip" title="в копии: %s">%s</span>' % (other_form, form)

        return jinja2.Markup(html)

    def get_property_html(self, header, text, alternative=None):

        if alternative is None or text == alternative:
            html = u'<div><h4>%(header)s</h4><p>%(text)s</p></div>'
            html = html % {'header': header, 'text': text}
        else:
            html = u'<div><h4><span class="changed-word" rel="tooltip" title="в копии: %(alternative)s">%(header)s</span></h4><p>%(text)s</p></div>'
            html = html % {'header': header, 'text': text, 'alternative': alternative}

        return jinja2.Markup(html)

    def get_property(self, property):
        if property in self.type.properties:
            if self.word.utg_word.properties.is_specified(property):
                return self.get_property_html(utg_relations.PROPERTY_TYPE.index_relation[property].text,
                                              self.word.utg_word.properties.get(property).text,
                                              self.other_version.utg_word.properties.get(property).text if self.other_version else None)
            elif self.type.properties[property]:
                return self.get_property_html(utg_relations.PROPERTY_TYPE.index_relation[property].text,
                                              u'<strong style="color: red;">необходимо указать</strong>',
                                              self.other_version.utg_word.properties.get(property).text if self.other_version else None)
            else:
                alternative = None
                if self.other_version and self.other_version.utg_word.properties.is_specified(property):
                    alternative = self.other_version.utg_word.properties.get(property).text

                return self.get_property_html(utg_relations.PROPERTY_TYPE.index_relation[property].text,
                                              u'может быть указано',
                                              alternative=alternative)

        return u''



STRUCTURES = { word_type: get_structure(word_type)
               for word_type in utg_relations.WORD_TYPE.records }
