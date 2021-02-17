from selene.support.shared import browser
from selene import have


def test_provides_common_todo_management():
    open_todomvc()

    add('a', 'b', 'c')
    todos_should_be('a', 'b', 'c')

    edit('b', 'b edited')

    toggle('b edited')
    clear_completed()
    todos_should_be('a', 'c')

    cancel_edit('c', 'to be canceled')

    delete('c')
    todos_should_be('a')


todos = browser.all('#todo-list>li')


def open_todomvc():
    browser.open('https://todomvc4tasj.herokuapp.com') \
        .should(have.js_returned(True,
             'return ($._data($("#clear-completed").get(0), "events")'
             '.hasOwnProperty("click") && '
             '(Object.keys(require.s.contexts._.defined).length === 39))'))


def add(*texts):
    for text in texts:
        browser.element('#new-todo').type(text).press_enter()


def todos_should_be(*with_texts):
    todos.should(have.exact_texts(*with_texts))


def todo(text):
    return todos.element_by(have.exact_text(text))


def start_editing(text, new_text):
    todo(text).double_click()
    return todos.element_by(have.css_class('editing'))\
        .element('.edit').set_value(new_text)


def edit(text, new_text):
    start_editing(text, new_text).press_enter()


def cancel_edit(text, new_text):
    start_editing(text, new_text).press_escape()


def toggle(text):
    todo(text).element('.toggle').click()


def clear_completed():
    browser.element('#clear-completed').click()


def delete(text):
    todo(text).hover().element('.destroy').click()
