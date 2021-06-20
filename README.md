# fleet-allocation-bin-packingish

Fun python script to help efficiently and evenly allocate fleets to systems that we want to defend.

I believe this problem is a spin on the bin-packing problem...

We have systems (the bins) we want to defend and we have fleets with varying powers that we want to pack into these bins/systems.
Each system has an artificial limit imposed upon it ... this is the total fleet power divided by the number of systems we want to defend

Traditionally we would want to find a lower bound to the bin-packing problem but in this case there isn't a need to as we have a predetermined number bins ... the number of systems we want to defend

I used the first-fit decreasing method to assign the fleets
