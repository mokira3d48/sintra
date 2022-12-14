import threading as th
from . import PROCESSES
from . import ERRO
from . import WARN


class Processing(th.Thread):
    """ 
    Structure of the processing implementation.
    """
    def __init__(self, *args, **kwargs):
        """ 
        Constructor of the keywords extraction program.
        """
        super(Processing, self).__init__(*args, **kwargs);
        self._params  = {};
        self._results = None;

    @property
    def results(self):
        """ 
        Return result of after program execution.
        """
        return self._results;

    def set_params(self, **kwargs):
        """ 
        Function that is used to set parametters of the program.
        """
        self._params.update({name:val for name, val in kwargs.items()});
        return kwargs;


def register(name=None):
    """
    Function decorator.
    """
    def make_registration(cls):
        """
        Function which makes registration of a process implemeted 
        to PROCESSES list.
        """
        # global name;
        global PROCESSES;

        if not issubclass(cls, Processing):
            raise TypeError(
                ERRO + "The processing which will be registered must be a sub class of the Processing class "
            );
        name_defined = name if name else cls.__name__;
        PROCESSES[name_defined] = cls;
        print(PROCESSES);
        print("OK");
        return cls;
    return make_registration;


def exec_process(args):
    """
    Function that is used to execute a process.
    """
    process_name = args.name;
    process      = PROCESSES.get(process_name);
    if process:
        process = process();
        process.set_params(**args.__dict__);
        process.run();
        process.show();
        return process.results;
    else:
        print(WARN + "Process selected not implemeted yet.");
        print(WARN + "python {} -h".format(__file__));
        return 0;

