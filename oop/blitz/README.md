# Быстрые вопросы - ответы

<details>
    <summary>Что такое спринт?</summary>

    Спринт – это фиксированный период времени, обычно от одной недели до месяца,
        в течение которого команда работает над задачами из бэклога.
        В процессе спринта проводятся ежедневные Scrum-встречи
        для синхронизации работы команды и обзора прогресса.
        К концу спринта команда создает и внедряет инкрементальную (пошаговую) версию продукта.
</details>

<details>
    <summary>Как организовывается спринт?</summary>

    Agile - это философия разработки, которая ставит в центр внимания коллективную работу,
    быструю адаптацию к изменениям, постоянную обратную связь и, самое главное, доставку ценности пользователям. 

    Scrum - это методология Agile, который основывается на итеративном процессе разработки с разделеннием на спринты.

    Kanban - это метод управления потоком работ, который использует визуальную доску, поделенную на несколько столбцов
    для отслеживания состояния задач (например: предстоящие задачи, в процессе разработки и в процессе тестирования).

    Issue, ticket - это термины, которые обозначают задачи, которые имеют приоритеты и
    которые необходимо выполнить в рамках проекта.

    Jira, Trello - это инструменты управления проектами, которые помогают командам эффективно отслеживать задачи и прогресс проекта.
</details>


### Задача: объединить два отсортированных списка.

```python
def merge_sorted_lists(list_1, list_2):
    merged_list = []
    i, j = 0, 0
    while i < len(list_1) and j < len(list_2):
        if list_1[i] < list_2[j]:
            merged_list.append(list_1[i])
            i += 1
        else:
            merged_list.append(list_2[j])
            j += 1

    merged_list.extend(list_1[i:])
    merged_list.extend(list_2[j:])
    return merged_list

list_1, list_2 = [1, 3, 5], [2, 4, 6]
merged_list = merge_sorted_lists(list_1, list_2)
print(merged_list)  # [1, 2, 3, 4, 5, 6]
```

### Задача: Найти подсписок максимальной суммы в списке

```python

def max_subarray_sum(arr):
    current_sum = 0
    current_subarray = []
    start_pos, end_pos = 0, 0

    max_sum = float('-inf')
    max_subarray = []
    max_start_pos, max_end_pos = 0, 0

    # Найти только максимальную сумму 
    # алгоритма Кадана
    # for val in arr:
    #   current_sum = max(current_sum + val, val)
    #   max_sum = max(max_sum, current_sum)
    
    for i, val in enumerate(arr):
        if current_sum + val > val:
            current_sum += val
            current_subarray.append(val)
            end_pos = i
        else:
            current_sum = val
            current_subarray = [val]
            start_pos, end_pos = i, i
        
        if current_sum > max_sum:
            max_sum = current_sum
            max_subarray = current_subarray[:]
            max_start_pos, max_end_pos = start_pos, end_pos
    
    return max_sum, max_subarray, max_start_pos, max_end_pos

nums = [1, -2, 3, -1, 2, 3]
nums2, max_sum, max_start_pos, max_end_pos = max_subarray_sum(nums)
print(nums2, max_sum, nums[max_start_pos:max_end_pos+1])  # 7 [3, -1, 2, 3] [3, -1, 2, 3]
```

### Подходы к решению алгоритмических задач:

**Разделяй и властвуй**:
  * Больше работает над подзадачами и, следовательно, требует больше времени.
  * подзадачи не зависят друг от друга.
```python
def fib(num):
  if num <= 2:
    return 1
  return fib(num-1) + fib(num-2)
```
**Динамическое программирование**:
  * Решает подзадачи только один раз, а затем сохраняет их в таблице.
  * подзадачи не являются независимыми.
  * метод "разделяй и властвуй" c кэшированием
```python
memo = {1: 1, 2: 1}
def fib(num):
  if num not in memo:
    memo[num] = fib(num-1) + fib(num-2)
  return memo[num]
```

Обе эти концепции рекурсивно разбивают проблему на подпроблемы одного и того-же типа до тех пор,
пока эти подпроблемы не станут достаточно легкими.\
Далее все решения подпроблем объединяются вместе для того, чтобы в итоге дать ответ на изначальную проблему.
