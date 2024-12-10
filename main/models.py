from django.db import models
from django.db.models import Manager, Q

# Honestly speaking, it's GPT output.

# The goal is to simplify query for optional fields
# For example, filter( Q(field=some_dict['some_field']) | Q(field=some_dict['some_field2']))
# And 'some_field' is None, that field will be excluded from the query
class CustomBaseManager(Manager):
    def _clean_q_objects(self, args):
        new_args = []
        for arg in args:
            if isinstance(arg, Q):
                # Build a new list of conditions for the Q object without None values
                new_children = [(k, v) for (k, v) in arg.children if v is not None]
                # Only add the Q object if it has valid conditions
                if new_children:
                    # Reconstruct the Q object with the filtered conditions
                    new_args.append(Q(*new_children, _connector=arg.connector, _negated=arg.negated))
            else:
                # If it's not a Q object, just keep it as is
                new_args.append(arg)
        return new_args

    def filter(self, *args, **kwargs):
        # Remove None values from kwargs
        filters = {key: value for key, value in kwargs.items() if value is not None}
        # Clean Q objects
        cleaned_args = self._clean_q_objects(args)
        # Call the parent's filter with cleaned arguments
        return super().filter(*cleaned_args, **filters)

    def exclude(self, *args, **kwargs):
        # Remove None values from kwargs
        filters = {key: value for key, value in kwargs.items() if value is not None}
        # Clean Q objects
        cleaned_args = self._clean_q_objects(args)
        # Call the parent's exclude with cleaned arguments
        return super().exclude(*cleaned_args, **filters)

class JobPosition(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class JobSkill(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value



