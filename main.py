# Importing the required libraries
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from haystack import Finder
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.retriever.sparse import TfidfRetriever
from haystack.pipeline import FAQPipeline

# Creating the mobile application class
class MyApp(MDApp):
    def build(self):
        # Creating the layout
        layout = BoxLayout(orientation='vertical')

        # Creating the label
        label = MDLabel(text="Ask me anything!", halign="center", theme_text_color="Secondary")

        # Creating the button
        button = MDFlatButton(text="Ask", on_release=self.ask_question)

        # Adding the label and button to the layout
        layout.add_widget(label)
        layout.add_widget(button)

        # Returning the layout
        return layout

    def ask_question(self, instance):
        # Getting the user's question
        user_question = input("Ask me: ")

        # Initializing the document store
        document_store = InMemoryDocumentStore()

        # Initializing the retriever
        retriever = TfidfRetriever(document_store=document_store)

        # Initializing the pipeline
        pipeline = FAQPipeline(retriever=retriever)

        # Initializing the finder
        finder = Finder(reader=None, retriever=retriever)

        # Indexing the documents
        documents = [
            {"text": "Sample document 1", "meta": {"name": "Document 1"}},
            {"text": "Sample document 2", "meta": {"name": "Document 2"}},
            {"text": "Sample document 3", "meta": {"name": "Document 3"}}
        ]
        document_store.write_documents(documents)

        # Searching for the answer
        prediction = finder.get_answers(question=user_question, top_k_retriever=3, top_k_reader=1)

        # Displaying the answer
        answer = prediction['answers'][0]['answer']
        self.show_dialog(answer)

    def show_dialog(self, answer):
        # Creating the dialog
        dialog = MDDialog(title="Answer", text=answer, size_hint=(0.8, 0.4))

        # Displaying the dialog
        dialog.open()

# Running the application
if __name__ == '__main__':
    MyApp().run()
