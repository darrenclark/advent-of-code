defmodule Oasis do
  def part1(path) do
    File.read!(path)
    |> String.split("\n")
    |> Enum.map(&String.split(&1, " "))
    |> Enum.map(&Enum.map(&1, fn x -> String.to_integer(x) end))
    |> Enum.map(&predict_next/1)
    |> Enum.sum()
    |> IO.inspect(label: "Sum of extrapolated values")
  end

  defp predict_next(history) do
    history
    |> Enum.reverse()
    |> expand()
    |> Enum.reverse()
    |> predict()
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

  defp predict([bottom | rest]), do: do_predict([0 | bottom], rest)

  defp do_predict(bottom, rest)

  defp do_predict([a |_], [[b | _]]) do
    a + b
  end

  defp do_predict([a |_], [[b | _] = new_bottom | rest]) do
    do_predict([a + b | new_bottom], rest)
  end
end
