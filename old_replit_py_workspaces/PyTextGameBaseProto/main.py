from region import Region
print(Region("Apple Airport", "airport"))

from story import Place, setworld, world, welcome

setworld(
	Place("Sarden", "world")
	.addactions("regiontravel")
	.addregion(
		Place("Sauria", "kingdom")
		.addactions("travel")
		.addregion(
			Place("Andrea", "town")
			.addactions("travel")
			.addregion(
				Place("Silver Sky", "tavern")
				.addactions("travel")
			)
			.addregion(
				Place("The Mercernary Guild", "guild")
				.addactions("travel")
			)
		)
		.addregion(
			Place("Shills", "town")
			.addactions("travel")
		)
	)
)

welcome()
print()
print(world().showactions(True))
print()
print(world().do(0).do(0))
