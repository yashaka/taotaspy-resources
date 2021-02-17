from selene.support.shared import browser
from selene import have

from tests.conftest import AtTodoMvcWithClearedStorageAfterEachTest


class TestUserWorkflow(AtTodoMvcWithClearedStorageAfterEachTest):

    def test_filtering(self):

        # open_todomvc()

        self.add('a', 'b', 'c')
        self.todos_should_be('a', 'b', 'c')

        self.toggle('b')

        # todo: this will be your task to finish this implementation;)

    def test_provides_common_todo_management(self):
        # open_todomvc()

        self.add('a', 'b', 'c')
        self.todos_should_be('a', 'b', 'c')

        self.edit('b', 'b edited')

        self.toggle('b edited')
        self.clear_completed()
        self.todos_should_be('a', 'c')

        self.cancel_edit('c', 'to be canceled')

        self.delete('c')
        self.todos_should_be('a')
