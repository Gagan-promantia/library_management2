# Copyright (c) 2025, Gagan G R and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PracticeDoc(Document):
	def after_insert(self):
		"""
        This runs automatically AFTER a new PracticeDoc is inserted
        Creates another document automatically (only once, no loop)
        """
        # Check if this document was auto-created (to prevent infinite loop)
		if self.description and 'auto-created' in self.description.lower():
			return  # Stop here, don't create another document
        
        # Create a related document automatically
		new_doc = frappe.get_doc({
            'doctype': 'PracticeDoc',
            'title': f'Auto Doc for {self.name}',
            'description': f'This was auto-created when {self.name} was inserted',
            'items': [
                {
				'item_name': 'Auto Item 1',
				'quantity': 10,
                    'remarks': 'Automatically added'
                }
            ]
        })
        
		new_doc.insert()
		frappe.db.commit()
        
		frappe.msgprint(f'Auto-created: {new_doc.name}')

		"""
        After creating a new document, 
        automatically update its description and save again
        """
        # Check if description is empty
		if not self.description:
            # Update description
			self.description = f"Document created on {frappe.utils.now()}"
            
            # Save the changes using doc.save()
			self.save()
            
			frappe.msgprint(f"✅ Description auto-updated and saved!")
	
		def delete_old_documents():
			"""
			Deletes all PracticeDoc documents older than 1 day
			"""
			from frappe.utils import add_days, now
			
			# Get documents created before yesterday
			old_docs = frappe.get_all('PracticeDoc', 
				filters={
					'creation': ['<', add_days(now(), -1)]
				},
				fields=['name']
			)
			
			deleted_count = 0
			for doc_info in old_docs:
				# Get the document
				doc = frappe.get_doc('PracticeDoc', doc_info.name)
				
				# Delete it
				doc.delete()
				deleted_count += 1
			
			frappe.db.commit()
			
			return f"Deleted {deleted_count} old documents"
		

		def validate(self):
			"""
			Compare current values with previous values
			"""
			# Get the document before any changes
			old_doc = self.get_doc_before_save()
			
			if old_doc:  # old_doc is None for new documents
				# Compare title
				if old_doc.title != self.title:
					frappe.msgprint(f"Title changed from '{old_doc.title}' to '{self.title}'")
				
				# Compare description
				if old_doc.description != self.description:
					frappe.msgprint(f"Description was updated!")
				
				# Compare number of items
				old_item_count = len(old_doc.items)
				new_item_count = len(self.items)
				
				if old_item_count != new_item_count:
					frappe.msgprint(f"Items changed: {old_item_count} → {new_item_count}")

			"""
			Check if specific fields changed
			"""
			# Check if title changed
			if self.has_value_changed('title'):
				frappe.msgprint(f"Title was changed!", indicator='blue')
			
			# Check if description changed
			if self.has_value_changed('description'):
				frappe.msgprint(f" Description was updated!", indicator='green')
			
			# Check if created_on changed (it shouldn't!)
			if self.has_value_changed('created_on'):
				frappe.msgprint(f" Created date was modified!", indicator='red')