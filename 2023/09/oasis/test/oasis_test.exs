defmodule OasisTest do
  use ExUnit.Case
  doctest Oasis

  test "greets the world" do
    assert Oasis.hello() == :world
  end
end
