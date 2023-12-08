const std = @import("std");

const Card = enum {
    _2,
    _3,
    _4,
    _5,
    _6,
    _7,
    _8,
    _9,
    _j,
    _q,
    _k,
    _a,
};

const Err = error{
    invalidArguments,
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer _ = gpa.deinit();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    if (args.len != 3) {
        std.debug.print("error: expected part1|part2 and file name", .{});
        return Err.invalidArguments;
    }

    const part = args[1];
    const inputFile = args[2];

    var result: i64 = 0;
    if (std.mem.eql(u8, part, "part1")) {
        result = part1(inputFile);
    } else {
        std.debug.print("error: expected part1 or part2", .{});
        return Err.invalidArguments;
    }

    const stdout = std.io.getStdOut().writer();

    try stdout.print("Result: {d}\n", .{result});
}

fn part1(inputFile: []u8) i64 {
    _ = inputFile;
    return 23;
}
