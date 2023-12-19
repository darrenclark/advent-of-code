package ca.darrenclark.adventofcode;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) throws IOException {
        var input = Files.lines(Path.of(args[0])).toList();
        Main m = new Main(input);
        m.parse();

        var part1 = m.evaluateParts().mapToInt(Part::totalRating).sum();

        System.out.println("[PART 1] Sum of ratings of accepted parts: " + part1);
    }

    record Part(int x, int m, int a, int s) {
        int get(String field) {
            switch (field) {
                case "x": return x;
                case "m": return m;
                case "a": return a;
                case "s": return s;
                default:
                    throw new RuntimeException("unexpected char");
            }
        }

        int totalRating() {
            return x + m + a + s;
        }
    }

    record Workflow(String name, List<Instruction> instructions) {}

    sealed interface Instruction permits BranchLessThan, BranchGreaterThan, Goto, Return {}
    record BranchLessThan(String field, int value, Instruction ifTrue) implements Instruction {}
    record BranchGreaterThan(String field, int value, Instruction ifTrue) implements Instruction {}
    record Goto(String workflow) implements Instruction {}
    record Return (boolean accepted) implements Instruction {}

    private List<String> input;
    private Map<String, Workflow> workflows = new HashMap<>();
    private List<Part> parts = new ArrayList<>();

    private Main(List<String> input) {
        this.input = input;
    }

    private Stream<Part> evaluateParts() {
        var in = workflows.get("in");
        return parts.stream().filter(part -> eval(part, in));
    }

    private boolean eval(Part part, Workflow workflow) {
        for (var instruction: workflow.instructions) {
            if (instruction instanceof BranchLessThan blt) {
                if (part.get(blt.field) < blt.value) {
                    instruction = blt.ifTrue;
                } else {
                    continue;
                }
            }
            if (instruction instanceof BranchGreaterThan btg) {
                if (part.get(btg.field) > btg.value) {
                    instruction = btg.ifTrue;
                } else {
                    continue;
                }
            }

            if (instruction instanceof Goto g) {
                return eval(part, workflows.get(g.workflow));
            } else if (instruction instanceof Return r) {
                return r.accepted;
            } else {
                throw new RuntimeException("Unexpected instruction");
            }
        }
        throw new RuntimeException("Unexpectedly ran out of instructions");
    }

    private void parse() {
        boolean parsingWorkflows = true;

        for (var s: input) {
            if (s.isEmpty()) {
                parsingWorkflows = false;
                continue;
            }

            if (parsingWorkflows) {
                var workflow = parseWorkflow(s);
                workflows.put(workflow.name, workflow);
            } else {
                parts.add(parsePart(s));
            }
        }
    }

    private Workflow parseWorkflow(String s) {
        var parts = s.split("[{}]");
        var name = parts[0];
        var instructions = Arrays.stream(parts[1].split(",")).map(this::parseInstruction).toList();
        return new Workflow(name, instructions);
    }

    private Instruction parseInstruction(String s) {
        if (s.contains(":")) {
            var parts = s.split(":");
            var cmp = parts[0];
            var cmpParts = cmp.split("[<>]");
            var field = cmpParts[0];
            var value = Integer.parseInt(cmpParts[1]);
            var ifTrue = parseInstruction(parts[1]);

            if (cmp.contains("<")) {
                return new BranchLessThan(field, value, ifTrue);
            } else {
                return new BranchGreaterThan(field, value, ifTrue);
            }
        } else if (s.equals("A")) {
            return new Return(true);
        } else if (s.equals("R")) {
            return new Return(false);
        } else {
            return new Goto(s);
        }
    }

    private Part parsePart(String str) {
        var split = new ArrayList<>(Arrays.asList(str.split("[{},=]")));
        split.remove("");

        int x = 0, m = 0, a = 0, s = 0;

        for (int i = 0; i < split.size(); i += 2) {
            var value = Integer.parseInt(split.get(i+1));
            switch (split.get(i)) {
                case "x":
                    x = value;
                    break;
                case "m":
                    m = value;
                    break;
                case "a":
                    a = value;
                    break;
                case "s":
                    s = value;
                    break;
                default:
                    throw new RuntimeException("unexpected char");
            }
        }

        return new Part(x, m, a, s);
    }
}