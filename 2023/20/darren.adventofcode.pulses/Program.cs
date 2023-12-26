if (args.Length != 1)
{
    Console.WriteLine("expected path to input");
    return 1;
}

var inputText = File.ReadAllText(args[0]);

var modules = inputText.Split('\n').Where(l => l.Length > 0).Select(Module (line) =>
{
    var parts = line.Split("->").ToList();

    var kind = parts[0][0];
    var name = parts[0].Trim('%', '&', ' ');

    var destinations = parts[1].Trim().Split(", ").ToList();

    if (name == "broadcaster")
    {
        return new Broadcaster(name, destinations);
    }
    else if (kind == '%')
    {
        return new FlipFlop(name, destinations);
    }
    else if (kind == '&')
    {
        return new Conjunction(name, destinations);
    }
    else
    {
        throw new Exception("unexpected input");
    }
}).ToList();

var machine = new Machine(modules);

for (int i = 0; i < 1000; i++)
{
    machine.PushButton();
}

var part1Answer = machine.HighPulsesSent * machine.LowPulsesSent;
Console.WriteLine("[PART 1] low pulses X high pulses = {0}", part1Answer);

return 0;

class Machine
{
    public Dictionary<string, Module> Modules { get; }

    public long HighPulsesSent { get; private set; }
    public long LowPulsesSent { get; private set; }

    public Machine(List<Module> modules)
    {
        Modules = modules.ToDictionary(m => m.Name);

        var inputsByDestination =
          modules
            .SelectMany(m => from d in m.Destinations select new { From = m.Name, To = d })
            .ToLookup(conn => conn.To, conn => conn.From);

        foreach (var m in modules)
        {
            if (m is Conjunction conj)
            {
                conj.Inputs = inputsByDestination[conj.Name].ToList();
            }
        }

        foreach (var entry in inputsByDestination) {
          if (!Modules.ContainsKey(entry.Key)) {
            Modules[entry.Key] = new Untyped(entry.Key);
          }
        }
    }

    public void PushButton()
    {
        var pulses = new Queue<Pulse>();
        pulses.Enqueue(new Pulse("button", "broadcaster", false));

        Pulse pulse;
        while (pulses.TryDequeue(out pulse))
        {
            if (pulse.IsHigh) HighPulsesSent += 1;
            else LowPulsesSent += 1;

            var newPulses = Modules[pulse.To].HandlePulse(pulse);
            newPulses.ForEach(pulses.Enqueue);
        }
    }
}

struct Pulse
{
    public string From { get; set; }
    public string To { get; set; }
    public bool IsHigh { get; set; }
    public bool IsLow
    {
        get { return !IsHigh; }
        set { IsHigh = !value; }
    }

    public Pulse(string from, string to, bool isHigh)
    {
        From = from;
        To = to;
        IsHigh = isHigh;
    }

    public override string ToString() => $"{From} -{(IsHigh ? "high" : "low")}-> {To}";
}

abstract class Module(string name, List<string> destinations)
{
    public string Name => name;
    public List<string> Destinations => destinations;

    public abstract List<Pulse> HandlePulse(Pulse pulse);

    protected List<Pulse> createPulses(bool isHigh) => Destinations.Select(d => new Pulse(Name, d, isHigh)).ToList();

    public override string ToString()
    {
        return Name + " -> " + string.Join(", ", Destinations);
    }
}

class Broadcaster(string name, List<string> destinations) : Module(name, destinations)
{
    public override List<Pulse> HandlePulse(Pulse pulse)
    {
        return createPulses(pulse.IsHigh);
    }
}

class FlipFlop(string name, List<string> destinations) : Module(name, destinations)
{
    public bool IsOn { get; set; }

    public override List<Pulse> HandlePulse(Pulse pulse)
    {
        if (pulse.IsHigh) return new List<Pulse>();

        if (IsOn)
        {
            IsOn = false;
            return createPulses(false);
        }
        else
        {
            IsOn = true;
            return createPulses(true);
        }
    }

    public override string ToString()
    {
        return "%" + base.ToString();
    }
}

class Conjunction(string name, List<string> destinations) : Module(name, destinations)
{
    private Dictionary<string, bool> _memory = new();

    private List<string> _inputs = new();
    public List<string> Inputs
    {
        get { return _inputs; }
        set
        {
            _inputs = value;
            _memory = new();
            foreach (var input in value)
            {
                _memory[input] = false;
            }
        }
    }

    private bool AreAllInputsHigh => _memory.Values.All(isHigh => isHigh);

    public override List<Pulse> HandlePulse(Pulse pulse)
    {
        _memory[pulse.From] = pulse.IsHigh;

        return createPulses(!AreAllInputsHigh);
    }

    public override string ToString()
    {
        return "&" + base.ToString() + " / inputs=[" + string.Join(", ", _inputs) + "]";
    }
}

class Untyped(string name) : Module(name, new())
{
    public override List<Pulse> HandlePulse(Pulse pulse)
    {
        return new();
    }
}
