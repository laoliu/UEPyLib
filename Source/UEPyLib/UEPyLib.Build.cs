// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class UEPyLib : ModuleRules
{
	public UEPyLib(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] {
			"Core",
			"CoreUObject",
			"Engine",
			"InputCore",
			"EnhancedInput",
			"AIModule",
			"StateTreeModule",
			"GameplayStateTreeModule",
			"UMG"
		});

		PrivateDependencyModuleNames.AddRange(new string[] {
            "PythonScriptPlugin",
            "UnrealEnginePython"
        });

		PublicIncludePaths.AddRange(new string[] {
			"UEPyLib",
			"UEPyLib/Variant_Platforming",
			"UEPyLib/Variant_Combat",
			"UEPyLib/Variant_Combat/AI",
			"UEPyLib/Variant_SideScrolling",
			"UEPyLib/Variant_SideScrolling/Gameplay",
			"UEPyLib/Variant_SideScrolling/AI"
		});

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });

		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
