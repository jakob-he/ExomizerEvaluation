from functools import wraps, partial

def print_status(label, width, cur, size):
    '''Print a statusbar.'''
    len_size = str(len(str(size)))
    # prevent division by zero by defaulting to 100% progress
    prog = round(cur/size * width) if size > 0 else 1
    print(
        ("\r{label}: \t[{prog: <"
         + str(width)
         + "}] {fin:>"+len_size+"}/{total:>"+len_size+"}").format(
             label=label,
             prog=("#"*prog),
             fin=cur,
             total=size
         ),
        end="")
        
def progress_bar(label, width=20):
    '''Build progressbar around yielding function.'''
    def progress_decorator(mapped_func):
        @wraps(mapped_func)
        def progress_wrapper(iterable, *args, **kwds):
            result = []
            size = len(iterable)

            for i, item in enumerate(iterable):
                print_status(label, width, i+1, size)
                result.append(mapped_func(item, *args, **kwds))
            print("")
            return result
        return progress_wrapper

    return progress_decorator
