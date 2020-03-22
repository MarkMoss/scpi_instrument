# Copyright 2020 Mark Moss
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to  
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.

import pyvisa

class ScpiInstrument():

    class CommandPart():
        def __init__(self, base, part, separator=None):
            """
            Constructor. 
            """
            self.__base = base;
            self.__part = part
            #Unless the caller specified a separator, use the separator 
            #specified by the base parameter.
            if separator is None:
                self.__separator = base.separator
            else: 
                self.__separator = separator
            #Use the visa instrument specified by the in all cases.
            self.__inst = base.visa_instrument
            #If base is a ScpiInstrument, then part contains the root of a
            #command.
            if isinstance(base, ScpiInstrument):
                self.__cmd = "{}".format(part)
            #Otherwise, splice part on the the base command using separator.
            else:
                self.__cmd = "{}{}{}".format(self.base, self.separator, self.part)


        @property
        def base(self):
            return self.__base
                    
        @property
        def command(self):
            return self.__cmd
        
        @property
        def part(self):
            return self.__part
        
        @property
        def separator(self):
            return self.__separator

        @property
        def visa_instrument(self):
            return self.__inst
            
        def __getattr__(self, name):
            setattr(self, name, self.__class__(self, name))
            return getattr(self, name)

        def __call__(self, *args, pre_param_separator=" ", param_separator=",", query_terminator="?"):
            #Check if this is a command (has args) or a query (no args)
            if args:
                c = "{}{}{}".format(self.command, pre_param_separator, param_separator.join(args)).strip()
                print("Command: {}".format(c))
                self.visa_instrument.write(c)
                return None
            else:
                c = "{}{}".format(self.command, query_terminator)
                print("Command: {}".format(c))
                r = self.visa_instrument.query(c)
                print("Response: {}".format(r))
        
        def __str__(self):
            return self.command
                            
        
    
    def __init__(self,
                 resource_name,
                 resource_manager=None,
                 access_mode=pyvisa.constants.AccessModes.no_lock,
                 open_timeout=0,
                 resource_pyclass=None):
        #Create a new resource manager if not specified in the parameters.
        if not resource_manager:
            self.__resource_manager = pyvisa.ResourceManager()
        else:
            self.__resource_manager = resource_manager
            
        #Open the instrument
        self.__inst = self.resource_manager.open_resource(resource_name,
                                                          access_mode,
                                                          open_timeout,
                                                          resource_pyclass)
    
    
    @property
    def separator(self):
        return ':'
    
    @property
    def resource_manager(self):
        return self.__resource_manager

    @property
    def visa_instrument(self):
        return self.__inst

    def __getattr__(self, name):
        setattr(self, name, self.CommandPart(self, name))
        return getattr(self, name)
