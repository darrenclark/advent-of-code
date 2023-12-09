defmodule Oasis do
  def part1(path) do
    File.read!(path)
    |> String.split("\n")
    |> Enum.map(&String.split(&1, " "))
    |> Enum.map(&Enum.map(&1, fn x -> String.to_integer(x) end))
    |> Enum.map(&extrapolate_forwards/1)
    |> Enum.sum()
    |> IO.inspect(label: "Sum of extrapolated values")
  end

  def part2(path) do
    File.read!(path)
    |> String.split("\n")
    |> Enum.map(&String.split(&1, " "))
    |> Enum.map(&Enum.map(&1, fn x -> String.to_integer(x) end))
    |> Enum.map(&extrapolate_backwards/1)
    |> Enum.sum()
    |> IO.inspect(label: "Sum of extrapolated values")
  end

  defp extrapolate_forwards(history) do
    history
    |> Enum.reverse()
    |> expand()
    |> Enum.reverse()
    |> predict_next()
  end

  defp extrapolate_backwards(history) do
    history
    |> Enum.reverse()
    |> expand()
    |> Enum.reverse()
    |> Enum.map(&Enum.reverse/1)
    |> predict_prev()
  end

  defp expand(history) do
    rest = Stream.unfold(history, fn line ->
      if Enum.all?(line, &(&1 == 0)) do
        nil
      else
        d = differences(line)
        {d, d}
      end
    end)

    Stream.concat([history], rest)
  end

  defp differences(line, acc \\ [])

  defp differences([a, b | rest], acc) do
    differences([b|rest], [(a - b)|acc])
  end

  defp differences(_, acc), do: Enum.reverse(acc)

  defp predict_next([bottom | rest]), do: do_predict_next([0 | bottom], rest)

  defp do_predict_next(bottom, rest)

  defp do_predict_next([a |_], [[b | _]]) do
    a + b
  end

  defp do_predict_next([a |_], [[b | _] = new_bottom | rest]) do
    do_predict_next([a + b | new_bottom], rest)
  end

  defp predict_prev([bottom | rest]), do: do_predict_prev([0 | bottom], rest)

  defp do_predict_prev(bottom, rest)

  defp do_predict_prev([a |_], [[b | _]]) do
    b - a
  end

  defp do_predict_prev([a |_], [[b | _] = new_bottom | rest]) do
    do_predict_prev([b - a | new_bottom], rest)
  end
end
