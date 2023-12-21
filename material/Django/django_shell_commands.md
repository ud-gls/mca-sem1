# Django Shell Commands for Database operations

Below is a list of common Django shell commands related to database operations, along with explanations and examples.

These commands are executed in the Django interactive shell (`python manage.py shell`) and are useful for interacting with the database.

**Note**: Make sure to replace myapp and MyModel with your actual app name and model name.

### Database Operations in Django Shell:

1. **Creating a new database record:**
   ```python
   from myapp.models import MyModel
   instance = MyModel(field1='value1', field2='value2')
   instance.save()
   ```

2. **Querying for records:**
   ```python
   from myapp.models import MyModel
   all_records = MyModel.objects.all()
   specific_record = MyModel.objects.get(id=1)
   filtered_records = MyModel.objects.filter(field='value')
   ```

3. **Updating a database record:**
   ```python
   instance = MyModel.objects.get(id=1)
   instance.field1 = 'new_value'
   instance.save()
   ```

4. **Deleting a database record:**
   ```python
   instance = MyModel.objects.get(id=1)
   instance.delete()
   ```

5. **Using the `create` method to create and save a record in one step:**
   ```python
   MyModel.objects.create(field1='value1', field2='value2')
   ```

6. **Filtering records using Q objects for complex queries:**
   ```python
   from django.db.models import Q
   MyModel.objects.filter(Q(field1='value1') | Q(field2='value2'))
   ```

7. **Aggregation functions (e.g., Count, Sum, Avg):**
   ```python
   from django.db.models import Count
   MyModel.objects.aggregate(record_count=Count('id'))
   ```

8. **Ordering records:**
   ```python
   ordered_records = MyModel.objects.order_by('field')
   ```

9. **Limiting the number of records returned:**
   ```python
   limited_records = MyModel.objects.all()[:5]
   ```

10. **Using `distinct` to get unique records:**
    ```python
    unique_records = MyModel.objects.values('field').distinct()
    ```

11. **Raw SQL queries:**
    ```python
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM myapp_mymodel")
        results = cursor.fetchall()
    ```

12. **Checking database table names:**
    ```python
    from myapp.models import MyModel
    table_name = MyModel._meta.db_table
    ```

13. **Checking database fields of a model:**
    ```python
    from myapp.models import MyModel
    field_names = MyModel._meta.get_fields()
    ```

14. **Checking the SQL statement for a queryset:**
    ```python
    queryset = MyModel.objects.filter(field='value')
    print(str(queryset.query))
    ```

15. **Using F expressions for database-level operations:**
    ```python
    from django.db.models import F
    MyModel.objects.filter(id=1).update(field=F('field') + 1)
    ```

16. **Using `select_related` for efficient ForeignKey queries:**
    ```python
    related_instance = MyModel.objects.select_related('related_model').get(id=1)
    ```

17. **Using `prefetch_related` for efficient ManyToMany queries:**
    ```python
    instances = MyModel.objects.prefetch_related('manytomany_field').all()
    ```

18. **Bulk insert using `bulk_create`:**
    ```python
    instances = [MyModel(field='value') for _ in range(100)]
    MyModel.objects.bulk_create(instances)
    ```

19. **Using `update` method to perform bulk updates:**
    ```python
    MyModel.objects.filter(field='old_value').update(field='new_value')
    ```

20. **Filtering records based on date fields:**
    ```python
    from datetime import date
    records_created_today = MyModel.objects.filter(created_at__date=date.today())
    ```

21. **Using `annotate` to add aggregated values to a queryset:**
    ```python
    from django.db.models import Count
    annotated_queryset = MyModel.objects.values('field').annotate(record_count=Count('id'))
    ```

22. **Filtering records based on a related model's field:**
    ```python
    records = MyModel.objects.filter(related_model__field='value')
    ```

23. **Using `exists` to check if a queryset has any results:**
    ```python
    has_records = MyModel.objects.filter(field='value').exists()
    ```

24. **Using `values` to retrieve specific fields in a queryset:**
    ```python
    values_list = MyModel.objects.values('field1', 'field2')
    ```

25. **Using `values_list` for a flat list of values:**
    ```python
    flat_list = MyModel.objects.values_list('field', flat=True)
    ```

26. **Handling NULL values with `isnull`:**
    ```python
    records_with_null = MyModel.objects.filter(field__isnull=True)
    ```

27. **Using `select_for_update` for row-level locking:**
    ```python
    with transaction.atomic():
        locked_instance = MyModel.objects.select_for_update().get(id=1)
    ```

28. **Creating a related object using the reverse relation:**
    ```python
    instance = MyModel.objects.get(id=1)
    instance.related_model_set.create(field='value')
    ```

29. **Rolling back a transaction:**
    ```python
    from django.db import transaction
    try:
        with transaction.atomic():
            # ... (database operations)
            raise Exception("Rollback!")
    except Exception as e:
        print(f"Exception: {e}")
    ```

30. **Using `get_or_create` to retrieve or create a record:**
    ```python
    instance, created = MyModel.objects.get_or_create(field='value', defaults={'other_field': 'other_value'})
    ```

31. **Using `distinct` with multiple fields:**
    ```python
    unique_records = MyModel.objects.values('field1', 'field2').distinct()
    ```

32. **Using `Case` to perform conditional queries:**
    ```python
    from django.db.models import Case, When
    queryset = MyModel.objects.annotate(
        result=Case(
            When(field='value', then='field1'),
            default='field2',
            output_field=models.CharField()
        )
    )
    ```

33. **Checking the number of records in a queryset:**
    ```python
    record_count = MyModel.objects.filter(field='value').count()
    ```

34. **Using `update_or_create` for updating or creating a record atomically:**
    ```python
    instance, created = MyModel.objects.update_or_create(
        field='value',
        defaults={'other_field': 'other_value'}
    )
    ```

35. **Performing case-insensitive queries:**
    ```python
    records = MyModel.objects.filter(field__iexact='value')
    ```

36. **Using `TruncDate` for grouping by date part:**
    ```python
    from django.db.models import Count, TruncDate
    records_by_date = MyModel.objects.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id'))
    ```

37. **Using `bulk_update` for efficiently updating multiple records:**
    ```python
    instances = MyModel.objects.filter(field='old_value')
    for instance in instances:
        instance.field = 'new_value'
    MyModel.objects.bulk_update(instances, ['field'])
    ```

38. **Checking the database connection status:**
    ```python
    from django.db import connections
    connection = connections['default']
    is_connected = connection.is_usable()
    ```

39. **Using `defer` to defer loading of specific fields:**
    ```python
    deferred_records = MyModel.objects.defer('field1', 'field2')
    ```

40. **Using `only` to load only specific fields:**
    ```python
    specific_fields = MyModel.objects.only('field1', 'field2')
    ```

**Django Filter Commands**:

1. **Basic Filtering:**
   ```python
   # Retrieve records where the field equals a specific value
   queryset = MyModel.objects.filter(field='value')
   ```

2. **Case-Insensitive Filtering:**
   ```python
   # Case-insensitive filtering
   queryset = MyModel.objects.filter(field__iexact='value')
   ```

3. **Filtering with Multiple Conditions (AND):**
   ```python
   # Retrieve records where multiple conditions are met (AND)
   queryset = MyModel.objects.filter(field1='value1', field2='value2')
   ```

4. **Filtering with Multiple Conditions (OR):**
   ```python
   from django.db.models import Q
   # Retrieve records where at least one condition is met (OR)
   queryset = MyModel.objects.filter(Q(field1='value1') | Q(field2='value2'))
   ```

5. **Negation (NOT) Filtering:**
   ```python
   # Retrieve records where a condition is not met
   queryset = MyModel.objects.exclude(field='value')
   ```

6. **Filtering with Date Fields:**
   ```python
   from datetime import date
   # Retrieve records based on date conditions
   queryset = MyModel.objects.filter(created_at__date=date.today())
   ```

7. **Filtering with Time Fields:**
   ```python
   from datetime import time
   # Retrieve records based on time conditions
   queryset = MyModel.objects.filter(updated_at__time=time(hour=8, minute=0))
   ```

8. **Filtering with DateTime Fields:**
   ```python
   from datetime import datetime
   # Retrieve records based on datetime conditions
   queryset = MyModel.objects.filter(updated_at__gt=datetime(2023, 1, 1))
   ```

9. **Filtering with NULL Values:**
   ```python
   # Retrieve records where a specific field is NULL
   queryset = MyModel.objects.filter(field__isnull=True)
   ```

10. **Filtering with Regex (Regular Expressions):**
    ```python
    # Retrieve records where a field matches a regular expression
    queryset = MyModel.objects.filter(field__regex=r'^[0-9]+$')
    ```

11. **Filtering with StartsWith, EndsWith, and Contains:**
    ```python
    # Retrieve records where a field starts with, ends with, or contains a specific value
    queryset_startswith = MyModel.objects.filter(field__startswith='prefix')
    queryset_endswith = MyModel.objects.filter(field__endswith='suffix')
    queryset_contains = MyModel.objects.filter(field__contains='substring')
    ```

12. **Filtering with In and Not In:**
    ```python
    # Retrieve records where a field is in or not in a list of values
    queryset_in = MyModel.objects.filter(field__in=['value1', 'value2'])
    queryset_not_in = MyModel.objects.exclude(field__in=['value1', 'value2'])
    ```

13. **Filtering with F Objects (Database-Level Operations):**
    ```python
    from django.db.models import F
    # Retrieve records based on database-level operations
    queryset = MyModel.objects.filter(field1__gt=F('field2'))
    ```

14. **Filtering with Case Expression:**
    ```python
    from django.db.models import Case, When
    # Filtering based on conditions using Case expressions
    queryset = MyModel.objects.annotate(
        result=Case(
            When(field='value1', then='field1'),
            default='field2',
            output_field=models.CharField()
        )
    )
    ```

15. **Filtering with `range`:**
    ```python
    # Retrieve records within a numeric range
    queryset = MyModel.objects.filter(field__range=(min_value, max_value))
    ```

16. **Filtering with `__exact` (Exact Match):**
    ```python
    # Retrieve records with an exact match (case-sensitive)
    queryset = MyModel.objects.filter(field__exact='value')
    ```

17. **Filtering with `__iexact` (Case-Insensitive Exact Match):**
    ```python
    # Retrieve records with an exact match (case-insensitive)
    queryset = MyModel.objects.filter(field__iexact='value')
    ```

18. **Filtering with `__gt`, `__lt`, `__gte`, `__lte` (Numeric Comparison):**
    ```python
    # Retrieve records with greater than, less than, greater than or equal to, and less than or equal to conditions
    queryset_gt = MyModel.objects.filter(field__gt=value)
    queryset_lt = MyModel.objects.filter(field__lt=value)
    queryset_gte = MyModel.objects.filter(field__gte=value)
    queryset_lte = MyModel.objects.filter(field__lte=value)
    ```

19. **Filtering with `__contains` (Case-Sensitive Contains):**
    ```python
    # Retrieve records where a field contains a substring (case-sensitive)
    queryset = MyModel.objects.filter(field__contains='substring')
    ```

20. **Filtering with `__icontains` (Case-Insensitive Contains):**
    ```python
    # Retrieve records where a field contains a substring (case-insensitive)
    queryset = MyModel.objects.filter(field__icontains='substring')
    ```

21. **Filtering with `__startswith` and `__endswith`:**
    ```python
    # Retrieve records where a field starts with or ends with a specific value
    queryset_startswith = MyModel.objects.filter(field__startswith='prefix')
    queryset_endswith = MyModel.objects.filter(field__endswith='suffix')
    ```

22. **Filtering with `__regex` (Regular Expression):**
    ```python
    # Retrieve records where a field matches a regular expression
    queryset = MyModel.objects.filter(field__regex=r'^[0-9]+$')
    ```

23. **Filtering with `__isnull`:**
    ```python
    # Retrieve records where a specific field is NULL or not NULL
    queryset_null = MyModel.objects.filter(field__isnull=True)
    queryset_not_null = MyModel.objects.filter(field__isnull=False)
    ```

24. **Filtering with `__day`, `__month`, `__year` (Date Components):**
    ```python
    # Retrieve records based on the day, month, or year of a date field
    queryset_day = MyModel.objects.filter(created_at__day=day_value)
    queryset_month = MyModel.objects.filter(created_at__month=month_value)
    queryset_year = MyModel.objects.filter(created_at__year=year_value)
    ```

25. **Filtering with `__week_day` (Day of the Week):**
    ```python
    # Retrieve records based on the day of the week (1 for Monday, 7 for Sunday)
    queryset = MyModel.objects.filter(created_at__week_day=weekday_value)
    ```

26. **Filtering with `__hour`, `__minute`, `__second` (Time Components):**
    ```python
    # Retrieve records based on the hour, minute, or second of a time field
    queryset_hour = MyModel.objects.filter(updated_at__hour=hour_value)
    queryset_minute = MyModel.objects.filter(updated_at__minute=minute_value)
    queryset_second = MyModel.objects.filter(updated_at__second=second_value)
    ```
