from sys import stdout, stderr;
from time import asctime;
from typing import Callable, Literal, TextIO;


class Debugger:
    STATIC: "Debugger" = None; # type: ignore
    DEBUG: "Debugger.Node" = None # type: ignore
    def __init__(self) -> None:
        if Debugger.STATIC is not None:
            self = Debugger.STATIC;
        else:
            self.debug_nodes: dict[str, list[Debugger.Node]] = {};
            self.debug_mode: Literal["ACTIVE","DUMP","INACTIVE"] = "INACTIVE";
            self.dump_location: TextIO = stderr;
            Debugger.STATIC = self;
            Debugger.DEBUG = Debugger.Node("debug");
        
    @staticmethod
    def start(dumping: bool = False) -> None:
        if Debugger.STATIC.debug_mode == "ACTIVE" and not dumping:
            raise RuntimeError("Debugger started as ACTIVE while in ACTIVE state");
        elif Debugger.STATIC.debug_mode == "DUMP" and dumping:
            raise RuntimeError("Debugger started as DUMP while in DUMP state");
        if not dumping:
            Debugger.STATIC.debug_mode = "ACTIVE";
        else:
            Debugger.STATIC.debug_mode = "DUMP";
        
    @staticmethod
    def start_dump(location: TextIO = stderr) -> None:
        if Debugger.STATIC.debug_mode != "DUMP": Debugger.STATIC.start(True);
        Debugger.STATIC.dump_location = location;
    
    @staticmethod
    def stop() -> None:
        Debugger.STATIC.debug_mode = "INACTIVE";
        
    @staticmethod
    def flush_logs(kill_nodes: bool = False, force_pretty: bool = False) -> None:
        if (not force_pretty) and (Debugger.STATIC.dump_location.name != stderr.name):
            Debugger.STATIC._plain_flush_logs(kill_nodes);
        else:
            Debugger.STATIC._pretty_flush_logs(kill_nodes);
        
    def _pretty_flush_logs(self, kill_nodes: bool = False) -> None:
        self.dump_location.write(f"{{\33[1m{asctime()}\33[0m}} \33[38;2;158;0;0m\33[1mFlushing DEBUG logs to {self.dump_location.name}...\33[0m\n");
        for namespace, nodes in self.debug_nodes.items():
            if namespace == "debug": continue;
            self.dump_location.write(f"\33[2m>>\33[0m '{namespace}' \33[2mnamespace\33[0m\n");
            for node in nodes:
                self.dump_location.write(f"| \33[2mexecution log\33[0m \33[2m<\33[0m{node.id}\33[2m> file <\33[0m{node.file}\33[2m>\33[0m\n");
                for log in node.logbook:
                    self.dump_location.write(f"| \33[2m|\33[0m \33[2m<\33[0m{log}\33[2m>\33[0m\n");
                node.logbook.clear();
            if kill_nodes: nodes.clear();
        self.dump_location.write("\33[38;2;158;0;0m\33[1mOperation Complete\33[0m\n\n");
        
    def _plain_flush_logs(self, kill_nodes: bool = False) -> None:
        self.dump_location.write(f"{{{asctime()}}} Flushing DEBUG logs to {self.dump_location.name}...\n");
        for namespace, nodes in self.debug_nodes.items():
            if namespace == "debug": continue;
            self.dump_location.write(f">> '{namespace}' namespace\n");
            for node in nodes:
                self.dump_location.write(f"| execution log <{node.id}> file <{node.file}>\n");
                for log in node.logbook:
                    self.dump_location.write(f"| | <{log}>\n");
                node.logbook.clear();
            if kill_nodes: nodes.clear();
        self.dump_location.write("Operation Complete\n\n");
        
    def _receive_node_log(self, file: str, log: str, force_pretty: bool = False) -> str:
        if (not force_pretty) and (self.dump_location.name != stderr.name) and (not self.debug_mode == "ACTIVE"):
            return self.__plain_receive_node_log(file, log);
        else:
            return self.__pretty_receive_node_log(file, log);
    
    def __plain_receive_node_log(self, file: str, log: str) -> str:
        if self.debug_mode == "ACTIVE":
            stdout.write(f"DEBUG:: {log}\n");
        elif self.debug_mode == "DUMP":
            self.dump_location.write(f"<{file}> {{{asctime()}}} DEBUG:: {log}\n");
        return log;
    
    def __pretty_receive_node_log(self, file: str, log: str) -> str:
        if self.debug_mode == "ACTIVE":
            stdout.write(f"\33[38;2;158;0;0m\33[1mDEBUG::\33[0m \33[2m{log}\33[0m\n");
        elif self.debug_mode == "DUMP":
            self.dump_location.write(f"\33[2m<\33[0m{file}\33[2m>\33[0m {{\33[1m{asctime()}\33[0m}} \33[38;2;158;0;0m\33[1mDEBUG::\33[0m \33[2m{log}\33[0m\n");
        return log;
        
    def _get_node_id(self, namespace: str) -> int:
        return len(self.debug_nodes.setdefault(namespace, []));
    
    def _set_node(self, node: "Debugger.Node"):
        self.debug_nodes[node.namespace].append(node);
        
    class Node:
        def __init__(self, namespace: str, file=__file__) -> None:
            self.namespace = namespace;
            self.file = file;
            self.id = Debugger.STATIC._get_node_id(namespace);
            self.logbook: list[str] = [];
            Debugger.STATIC._set_node(self);
        
        def __call__(self, title: str, value: object) -> None:
            self.logbook.append(Debugger.STATIC._receive_node_log(self.file, f"'{self.namespace}:{title}' {value}"));

def DebugNode(namespace: str) -> Callable[[str,object],None]:
    _ = Debugger().Node(namespace);
    Debugger.DEBUG(f"[{namespace}].node-id", _.id);
    return _;

def foo() -> int:
    Debug = DebugNode("foo");
    ...
    bar: int = 87;
    ...
    Debug("bar",bar);
    Debug("bar-modified",bar * 32 - 17);
    return bar;
    
print(foo());

Debugger.start_dump(open("debugger_flush_test.log", "a"));
#Debugger.start();

print(foo());

Debugger.flush_logs();

print(foo());

Debugger.flush_logs(True);
Debugger.flush_logs();

"""
I want to use something like :

def foo(...) -> ...:
    Debug = DebugNode("foo");
    ...
    x: ... = ...;
    ...
    Debug("x",x);
    ...
"""
    
    