/* Copyright 2026  Simeon Ehrig.
 * SPDX-License-Identifier: ISC
 */

#include <alpaka/alpaka.hpp>

#include <iostream>

using namespace alpaka;

using Vec2D = Vec<std::size_t, 2>;

struct GameOfLife
{
    constexpr auto operator()(concepts::SimdPtr auto const& elem) const
    {
        using SimdType = typename ALPAKA_TYPEOF(elem.load());
        auto sum = elem[Vec2D{-1, -1}].load() + elem[Vec2D{-1, 0}].load() + elem[Vec2D{-1, 1}].load()
                   + elem[Vec2D{0, -1}].load() + elem[Vec2D{0, 1}].load() + elem[Vec2D{1, -1}].load()
                   + elem[Vec2D{1, 0}].load() + elem[Vec2D{1, 1}].load();

        if(where(elem.load() == SimdType::fill(1), true))
        {
            return 0;
        }
        return elem.load();
    }
};

void print_world(alpaka::concepts::IDataSource auto const& world)
{
    static_assert(ALPAKA_TYPEOF(world)::dim() == 2);
    for(std::size_t y = 0; y < world.getExtents()[0]; ++y)
    {
        for(std::size_t x = 0; x < world.getExtents()[1]; ++x)
        {
            if(world[Vec{y, x}] == 0)
            {
                std::cout << ". ";
            }
            else
            {
                std::cout << "x ";
            }
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

auto example(auto const deviceSpec, auto const exec) -> int
{
    std::cout << "Using alpaka accelerator: " << onHost::demangledName(exec) << " for "
              << deviceSpec.getApi().getName() << " " << deviceSpec.getDeviceKind().getName() << std::endl;
    // We use a square world. Each site has the size.
    constexpr std::size_t site_size = 10;
    // Add 2 to each site for the halo
    constexpr Vec2D extents{site_size + 2, site_size + 2};

    auto deviceSelector = onHost::makeDeviceSelector(deviceSpec);
    onHost::Device device = deviceSelector.makeDevice(0);
    onHost::Queue queue = device.makeQueue();


    auto bufHost = onHost::allocHost<int>(Vec2D{site_size, site_size});
    onHost::memset(queue, bufHost, 0);
    onHost::wait(queue);

    // .x.
    // ..x
    // xxx
    bufHost[Vec2D{0, 1}] = 1;
    bufHost[Vec2D{1, 2}] = 1;
    bufHost[Vec2D{2, 0}] = 1;
    bufHost[Vec2D{2, 1}] = 1;
    bufHost[Vec2D{2, 2}] = 1;

    print_world(bufHost);

    auto bufA = onHost::alloc<int>(device, Vec2D{site_size + 2, site_size + 2});
    auto bufB = onHost::alloc<int>(device, Vec2D{site_size + 2, site_size + 2});
    auto coreViewA = bufA.getSubView(Vec2D{1, 1}, Vec2D{site_size, site_size});
    auto coreViewB = bufB.getSubView(Vec2D{1, 1}, Vec2D{site_size, site_size});

    onHost::memset(queue, bufB, 0);
    onHost::memcpy(queue, coreViewA, bufHost);

    onHost::transform(queue, exec, coreViewB, StencilFunc{GameOfLife{}}, coreViewA);
    onHost::memcpy(queue, bufHost, coreViewB);
    onHost::wait(queue);

    print_world(bufHost);
    return 0;
}

auto main(int argc, char* argv[]) -> int
{
    return onHost::executeForEachIfHasDevice(
        [=](auto const& backend)
        { return example(backend[alpaka::object::deviceSpec], backend[alpaka::object::exec]); },
        onHost::allBackends(onHost::enabledDeviceSpecs, exec::enabledExecutors));
}
